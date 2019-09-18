from django.contrib import admin
from .models import item, orderitem, order

admin.site.register(item)

admin.site.register(orderitem)

admin.site.register(order)