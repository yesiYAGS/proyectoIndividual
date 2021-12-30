from django.contrib import admin
from .models import Adicional, AdicionalOrden, Orden, Producto
# Register your models here.

admin.site.register(Producto)
admin.site.register(Adicional)
admin.site.register(AdicionalOrden)
admin.site.register(Orden)
