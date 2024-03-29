from django.contrib import admin
from products.models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=["name","slug","created","modified"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "category",
        "price",
        "inventory",
        "is_available",
        "created",
        "modified",
    ]
    list_filter = ["is_available", "created", "modified"]
    list_editable = ["price", "is_available","inventory"]