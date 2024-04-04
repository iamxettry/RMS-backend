from django.db import models
from decimal import Decimal


# model for order

class Order(models.Model):
    account=models.ForeignKey('auth_user_account.accountUser', on_delete=models.CASCADE)
    menu_item=models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add=True)
    quantity = models.FloatField()
    totalPrice=models.FloatField(blank=True,null=True)
    complete=models.BooleanField(default=False)

    class Meta:
        verbose_name="Order"
        verbose_name_plural="Orders"
    
    def _str_(self):
        return f"{self.account.username}'s Order :{self.menu_item.name}"

    def save(self,*args, **kwargs):
        quantity_decimal=Decimal(str(self.quantity))
        price_decimal=Decimal(str(self.menu_item.price))

        # total price

        self.totalPrice=quantity_decimal*price_decimal
        super(Order, self).save(*args,**kwargs)





# model for cart
class Cart(models.Model):
    u_id=models.ForeignKey('auth_user_account.accountUser', on_delete=models.CASCADE )
    f_id=models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE)
    quantity=models.FloatField()
    totalPrice=models.FloatField(blank=True,null=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f"{self.u_id.username}'s Order: {self.f_id.name}"
    
    def save(self, *args, **kwargs):
        # Convert the quantity and price to Decimal
        quantity_decimal = Decimal(str(self.quantity))
        price_decimal = Decimal(str(self.f_id.price))
        
        # Calculate the total price as a Decimal
        self.totalPrice = quantity_decimal * price_decimal
        super(Cart, self).save(*args, **kwargs)
