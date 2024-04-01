from django.db import models
from django.db.models import Avg, Sum

from api.utils import OrderStatus
from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=25)
    parent_category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=OrderStatus.choices(),
    )
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"order {self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_cost = self.order.items.aggregate(
            total_cost=Sum(models.F("quantity") * models.F("product__price"))
        )["total_cost"]
        self.order.total_cost = total_cost or 0  # Handle case where total_cost is None
        self.order.save()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    value = models.DecimalField(max_digits=3, decimal_places=2)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        avg_rating = self.product.reviews.aggregate(avg_rating=Avg("value"))[
            "avg_rating"
        ]
        if avg_rating:
            self.product.rating = round(avg_rating, 2)
        else:
            self.product.rating = None

        self.product.save()
