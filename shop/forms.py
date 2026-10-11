from django import forms
from django.contrib.auth.models import User
from .models import Product, Customer, Sale


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "quantity", "buying_price", "selling_price"]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "location"]


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["product", "quantity", "selling_price", "payment_method", "customer"]

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.fields["product"].queryset = Product.objects.filter(quantity__gt=0)
        self.fields["customer"].required = False
        self.fields["quantity"].min_value = 1

    def clean(self):
        d = super().clean()
        p, q = d.get("product"), d.get("quantity")
        if p and q:
            if q < 1:
                self.add_error("quantity", "Enter at least 1 piece.")
            elif q > p.quantity:
                self.add_error("quantity", f"Only {p.quantity} pc of {p.name} left in stock.")
        return d


class CashierForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)

    class Meta:
        model = User
        fields = ["first_name", "username", "password"]
        labels = {"first_name": "Full name"}
