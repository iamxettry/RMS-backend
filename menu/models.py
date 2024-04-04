from django.db import models

class MenuItem(models.Model):
    VEG = 'VEG'
    NON_VEG = 'NON_VEG'
    NONE = 'NONE'

    TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
        (NONE, 'None of them'),
    ]
    name=models.CharField('Name',max_length=50)
    category=models.CharField('Category', max_length=30)
    price=models.DecimalField('Price',max_digits=6, decimal_places=1)
    itemtype=models.CharField(max_length=8,choices=TYPE_CHOICES, default=None)
    img=models.ImageField(blank=True,null=True,upload_to='menu_images/')
    availables=models.BooleanField(False)
    calorie=models.IntegerField(blank=True)
