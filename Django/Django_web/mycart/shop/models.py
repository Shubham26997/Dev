from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    '''
    By default model have a ID field auto generated so no need to have a separate field,\
    if required then define the field with primary_key=True so that django,\
    will delete the by_default key from DB and keep your defined field as main ID field'''

    product_id = models.AutoField("ID", primary_key=True, unique=True)
    product_name = models.CharField("Product Name", max_length=20, null=False, blank=False)
    product_description = models.CharField("Product Description", max_length=100, null=True, blank=True)
    publish_date = models.DateField("Publish Date", default=timezone.now())
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=60, default="")
    price = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to="shop/images", default="")
    # product_image = models.FileField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name