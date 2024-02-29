from django.contrib import admin

from .models import Car, Country, Commentary, Manufacture

# Register your models here.

admin.site.register(Car)
admin.site.register(Manufacture)
admin.site.register(Country)
admin.site.register(Commentary)
