from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    quantity = models.PositiveIntegerField("Stock now (pc)", default=0)
    opening_quantity = models.PositiveIntegerField(default=0, editable=False)
    buying_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    location = models.CharField(max_length=160)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Sale(models.Model):
    PAYMENT = [("Cash", "Cash"), ("Mobile Money", "Mobile Money"), ("Bank/Card", "Bank/Card")]
    created = models.DateTimeField(auto_now_add=True)
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField("Number of pieces")
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    buying_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=14, decimal_places=2, editable=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT, default="Cash")

    class Meta:
        ordering = ["-created"]

    @property
    def profit(self):
        return (self.selling_price - self.buying_price) * self.quantity
