from django.contrib import admin
from shop.models import Product
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ["product_id","product_name", "publish_date"]
    search_fields = ["product_name", "product_id"]
    list_filter = ["publish_date"]

# admin.site.register(Product)
