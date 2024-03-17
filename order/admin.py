from django.contrib import admin
from .models import Cart

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display=['id','u_id','f_id','quantity','totalPrice' ]


admin.site.register(Cart,CartAdmin)