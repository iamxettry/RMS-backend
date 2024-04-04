from django.contrib import admin
from .models import MenuItem

# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display=['id','name','category','price','itemtype','img','availables','calorie' ]


admin.site.register(MenuItem,MenuAdmin)