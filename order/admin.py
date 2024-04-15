from django.contrib import admin
from .models import Cart,Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','account','menu_item','order_date','quantity','totalPrice','complete', 'paid']
class CartAdmin(admin.ModelAdmin):
    list_display=['id','u_id','f_id','quantity','totalPrice' ]


admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)