from django.contrib import admin
from .models import Customer, Restaurant, Order, Item, Payment, SearchedDate

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'cname', 'caddress']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['rname', 'raddress']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'order_number', 'order_placed_at', 'order_delivered_at', 'order_status', 'customer', 'order_total']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'iname', 'quantity', 'price']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'items_total', 'packing_charges', 'platform_fee', 'delivery_partner_fee', 'discount_applied', 'taxes', 'order_total']

@admin.register(SearchedDate)
class SearchedDateAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_date', 'till_date')