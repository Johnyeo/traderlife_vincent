from django.contrib import admin
from sign.models import *

# Register your models here.

class MarketGoodsAdmin(admin.ModelAdmin):
    list_display = ['name','price','count','status','flag','create_time','price_scope']

class MyGoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'count', 'status','flag','username','create_time']

class EventsAdmin(admin.ModelAdmin):
    list_display = ['name','comment','type','status','flag','create_time']

admin.site.register(Market_goods,MarketGoodsAdmin)
admin.site.register(My_goods, MyGoodsAdmin)
admin.site.register(Event, EventsAdmin)