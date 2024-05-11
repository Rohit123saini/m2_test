from django.contrib import admin

from .models import product_management,UserProduct,shiping_detail,ordered


admin.site.register(product_management)
admin.site.register(UserProduct)
admin.site.register(shiping_detail)
admin.site.register(ordered)