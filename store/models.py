from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null = True, blank= True, on_delete=models.CASCADE)
    admin = models.BooleanField(default = False)
    name = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Catagories(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Brands(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Product(models.Model):
    name = models.CharField(max_length=50, null=True)
    price = models.FloatField()
    details = models.CharField(max_length=150, null=True)
    image = models.ImageField(null=True, blank=True)
    catagoryId = models.ForeignKey(Catagories, null=True, blank=True, on_delete=models.CASCADE)
    brandId = models.ForeignKey(Brands,null=True, blank = True,  on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank = True, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default = False)
    transaction_id = models.CharField(max_length=100,  null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank = True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, blank = True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 0, null=True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank = True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, blank = True, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default = 0, null=True, blank = True)

    def __str__(self):
        return self.address