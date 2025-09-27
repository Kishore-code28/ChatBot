from django.db import models


class Products(models.Model):
    product_id = models.IntegerField(primary_key= True,)
    customer_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    price = models.IntegerField()