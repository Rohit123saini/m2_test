from django.db import models
from django.contrib.auth.models import User
class product_management(models.Model):
    name=models.CharField(max_length=50,null=False)
    description=models.CharField(max_length=500,null=False)
    price=models.IntegerField(null=False)
    quantity=models.IntegerField(null=False)
    image=models.ImageField(upload_to='image/',null=False)
    def __str__(self):
        return self.name


class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product_management, on_delete=models.CASCADE)
    quantities = models.PositiveIntegerField(default=1)
    total_price=models.PositiveIntegerField(default=1)


class shiping_detail(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    email=models.EmailField()
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=30)
    card=models.CharField(max_length=20)
    expiry=models.CharField(max_length=10)
    cvv=models.CharField(max_length=10)


class ordered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(product_management,on_delete=models.CASCADE)
    total_price=models.IntegerField()
    choice=[
        ('cancel','cancel'),
        ('packing','packing'),
        ('shipping','shipping'),
        ('delivered','delivered')
    ]

    status=models.CharField(max_length=30,choices=choice)
    ordered = models.DateTimeField(auto_now_add=True)