from django.contrib import admin
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, Category, Invoice, Dispatch, subcategory
# Register your models here.
def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ordered',
        'being_delivered', 
        'received', 
        'refund_requested', 
        'refund_granted',
        'billing_address',
        'shipping_address',
        'payment',
        'coupon'
        ]

    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'    
    ]

    list_filter = [
        'user', 
        'ordered', 
        'being_delivered', 
        'received', 
        'refund_requested', 
        'refund_granted'
        ]
    
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip'
    ]

    list_filter = ['country']
    search_fields = ['user__username','street_address','apartment_address','zip']

admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address, AddressAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Category)
admin.site.register(Invoice)
admin.site.register(Dispatch)
admin.site.register(subcategory)