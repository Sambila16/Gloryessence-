from django.contrib.auth import views as auth
from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.home, name="home"),
    path("login/", auth.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
    path("dashboard/", v.dashboard, name="dashboard"),
    path("sales/new/", v.sale_new, name="sale_new"),
    path("sales/", v.sales, name="sales"),
    path("customers/", v.customers, name="customers"),
    path("customers/new/", v.customer_new, name="customer_new"),
    path("products/", v.products, name="products"),
    path("products/new/", v.product_edit, name="product_new"),
    path("products/<int:pk>/", v.product_edit, name="product_edit"),
    path("cashiers/", v.cashiers, name="cashiers"),
    path("cashiers/<int:pk>/toggle/", v.cashier_toggle, name="cashier_toggle"),
    path("report/", v.report, name="report"),
]
