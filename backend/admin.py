from django.contrib import admin

from backend.models import Addresses, PointCoefficients, Users

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    ...

class AddressAdmin(admin.ModelAdmin):
    ...

class PointCoefficientsAdmin(admin.ModelAdmin):
    ...

admin.site.register(Users, UsersAdmin)
admin.site.register(Addresses, AddressAdmin)
admin.site.register(PointCoefficients, PointCoefficientsAdmin)
