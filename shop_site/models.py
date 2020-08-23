from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django.utils import timezone

LABEL_CHOICES = (
    ('P', 'NEW'),
    ('S', 'BestSeller'),
    ('D', 'Deal Of The Day')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)    
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    sub_category = models.ForeignKey('subcategory', on_delete=models.SET_NULL, blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True, null=True)
    item_image = models.ImageField(upload_to="item_image", blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    category_title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_price(self):
        if self.item.discount_price:
            total_price = self.quantity * self.item.discount_price
        else:
            total_price = self.quantity * self.item.price
        
        return total_price

    def get_quantity(self):
        qtn = self.quantity
        return qtn


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(default=timezone.now)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address' , on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey('Address', related_name='billing_address' , on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_bill_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()

        if self.coupon is not None:
            coupon_price = (total/100) * self.coupon.discount_percentage
            total -= coupon_price

        return total

    def get_discounted_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()

        coupon_price = (total/100) * self.coupon.discount_percentage

        return coupon_price
    
    def get_total_quantity(self):
        total_qtn = 0
        for order_item in self.items.all():
            total_qtn += order_item.get_quantity()

        return total_qtn

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_current_authenticated_user)
    street_address = models.CharField(max_length=150)
    apartment_address = models.CharField(max_length=150)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    discount_percentage = models.IntegerField()
    valid_from = models.DateTimeField(null=True)
    valid_till = models.DateTimeField(null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f'{self.id}'

class subcategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory_title = models.CharField(max_length=100)

    def __str__(self):
        return self.subcategory_title

class Invoice(models.Model):
    InvoiceId = models.CharField(primary_key=True, max_length=15)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, unique=True)
    order_ref_code = models.CharField(max_length=20)
    amount_paid = models.IntegerField()

    def __str__(self):
        return self.InvoiceId

class Dispatch(models.Model):
    docketno = models.CharField(max_length=15)
    transpoter_name = models.CharField(max_length=100)
    dispatch_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.transpoter_name