from django.contrib import admin
from .models import Product, Order, OrderItem, Manufacturer, Review, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Manufacturer)
admin.site.register(Review)
admin.site.register(Category)
