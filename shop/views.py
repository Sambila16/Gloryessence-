from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CashierForm, CustomerForm, ProductForm, SaleForm
from .models import Customer, Product, Sale


def admin_required(view):
    @login_required
    def wrapper(request, *a, **k):
        if not request.user.is_staff:
            messages.error(request, "That page is for the admin only.")
            return redirect("home")
        return view(request, *a, **k)
    wrapper.__name__ = view.__name__
    return wrapper


def filtered_sales(request, qs):
    d1, d2, c = (request.GET.get(x, "") for x in ("from", "to", "cashier"))
    if d1:
        qs = qs.filter(created__date__gte=d1)
    if d2:
        qs = qs.filter(created__date__lte=d2)
    if c and request.user.is_staff:
        qs = qs.filter(cashier_id=c)
    return qs


def home(request):
    # Visitors see the welcome page; logged-in users go straight to their work.
    if request.user.is_authenticated:
        return redirect("dashboard" if request.user.is_staff else "sale_new")
    return render(request, "shop/index.html")


@admin_required
def dashboard(request):
    today = Sale.objects.filter(created__date=timezone.localdate()).select_related("cashier", "product")
    by_cashier = {}
    for s in today:
        row = by_cashier.setdefault(s.cashier, {"count": 0, "total": Decimal(0)})
        row["count"] += 1
        row["total"] += s.total
    return render(request, "shop/dashboard.html", {
        "total": sum((s.total for s in today), Decimal(0)),
        "profit": sum((s.profit for s in today), Decimal(0)),
        "count": today.count(),
        "by_cashier": by_cashier.items(),
        "low_stock": Product.objects.filter(quantity__lte=5),
        "recent": today[:8],
    })


@login_required
def sale_new(request):
    form = SaleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            sale = form.save(commit=False)
            product = Product.objects.get(pk=sale.product_id)
            if sale.quantity > product.quantity:
                form.add_error("quantity", "Stock changed. Check the quantity again.")
            else:
                sale.cashier = request.user
                sale.buying_price = product.buying_price
                sale.total = sale.selling_price * sale.quantity
                sale.save()
                product.quantity -= sale.quantity
                product.save()
                messages.success(request, f"Recorded: {sale.quantity} x {product.name} = {sale.total:,.0f}")
                return redirect("sale_new")
    prices = {p.pk: str(p.selling_price) for p in Product.objects.all()}
    mine = Sale.objects.filter(cashier=request.user, created__date=timezone.localdate()).select_related("product")[:8]
    return render(request, "shop/sale_form.html", {"form": form, "prices": prices, "recent": mine})


@login_required
def sales(request):
    qs = Sale.objects.select_related("product", "cashier", "customer")
    if not request.user.is_staff:
        qs = qs.filter(cashier=request.user)
    qs = filtered_sales(request, qs)
    return render(request, "shop/sales.html", {
        "sales": qs, "total": qs.aggregate(t=Sum("total"))["t"] or 0,
        "cashiers": User.objects.filter(is_staff=False), "get": request.GET,
    })


@login_required
def customers(request):
    q = request.GET.get("q", "")
    qs = Customer.objects.select_related("added_by")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(location__icontains=q))
    return render(request, "shop/customers.html", {"customers": qs, "q": q})


@login_required
def customer_new(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        c = form.save(commit=False)
        c.added_by = request.user
        c.save()
        messages.success(request, f"Customer {c.name} saved.")
        return redirect("customers")
    return render(request, "shop/form.html", {"form": form, "title": "Register regular customer"})


@admin_required
def products(request):
    return render(request, "shop/products.html", {"products": Product.objects.all()})


@admin_required
def product_edit(request, pk=None):
    obj = get_object_or_404(Product, pk=pk) if pk else None
    old_qty = obj.quantity if obj else 0
    old_open = obj.opening_quantity if obj else 0
    form = ProductForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        p = form.save(commit=False)
        p.opening_quantity = max(old_open + p.quantity - old_qty, 0)
        p.save()
        messages.success(request, f"{p.name} saved.")
        return redirect("products")
    return render(request, "shop/form.html", {"form": form, "title": "Edit product" if obj else "Register product",
                  "hint": "Changing the stock number adds or removes pieces from capital." if obj else ""})


@admin_required
def cashiers(request):
    form = CashierForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        User.objects.create_user(form.cleaned_data["username"], password=form.cleaned_data["password"],
                                 first_name=form.cleaned_data["first_name"])
        messages.success(request, "Cashier account created.")
        return redirect("cashiers")
    return render(request, "shop/cashiers.html", {"form": form, "cashiers": User.objects.filter(is_staff=False)})


@admin_required
def cashier_toggle(request, pk):
    u = get_object_or_404(User, pk=pk, is_staff=False)
    if request.method == "POST":
        u.is_active = not u.is_active
        u.save()
    return redirect("cashiers")


@admin_required
def report(request):
    sales_qs = filtered_sales(request, Sale.objects.all())
    sold, profit = {}, {}
    for s in sales_qs:
        sold[s.product_id] = sold.get(s.product_id, 0) + s.quantity
        profit[s.product_id] = profit.get(s.product_id, Decimal(0)) + s.profit
    rows, tc, tp = [], Decimal(0), Decimal(0)
    for p in Product.objects.all():
        cap = p.opening_quantity * p.buying_price
        pr = profit.get(p.pk, Decimal(0))
        rows.append({"p": p, "sold": sold.get(p.pk, 0), "capital": cap, "profit": pr, "new_capital": cap + pr})
        tc += cap
        tp += pr
    return render(request, "shop/report.html", {
        "rows": rows, "tc": tc, "tp": tp, "tn": tc + tp,
        "cashiers": User.objects.filter(is_staff=False), "get": request.GET,
    })
