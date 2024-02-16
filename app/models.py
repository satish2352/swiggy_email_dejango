from django.db import models
from django.contrib.auth.models import User
import datetime

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cname = models.CharField(max_length=255)
    caddress = models.TextField()

    def __str__(self):
        return f"{self.cname}-{self.user}" 

class SearchedDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField(null=True,blank=True)
    till_date = models.DateField(default=datetime.date(2014, 1, 1), null=True)

    def __str__(self):
        return f'{self.user.username} - {self.from_date} to {self.till_date}'
class Restaurant(models.Model):
    rname = models.CharField(max_length=255,blank=True,null=True,default='not Found')
    raddress = models.TextField()

    def __str__(self):
        return self.rname

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, unique=True)
    order_placed_at = models.DateTimeField()
    order_delivered_at = models.DateTimeField()
    order_status = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return f"Order {self.order_number} - {self.order_placed_at} -{self.customer.user}"
    

class Item(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    iname = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # itotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.iname} (₹{self.price} each)"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    items_total = models.DecimalField(max_digits=8,decimal_places=2,null = True , blank=2)
    packing_charges = models.DecimalField(max_digits=8, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True, default=0 )
    delivery_partner_fee = models.DecimalField(max_digits=8, decimal_places=2)  
    discount_applied = models.DecimalField(max_digits=8, decimal_places=2)
    taxes = models.DecimalField(max_digits=8, decimal_places=2)
    order_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Payment for Order {self.order.order_number} - {self.payment_method}"
