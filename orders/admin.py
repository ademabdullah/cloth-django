from django.contrib import admin
from .models import Payment, OrderProduct, Order
# Register your models here.


''' This class appends the related orderProduct
    table to the products table '''

class OrderProductInline (admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price')
    extra = 0

''' This class determines how orders are displayed on the
    Orders GUI admin page '''

class OrderAdmin (admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'order_total', 'tax', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
