from django.contrib import admin

from backend.models import Users

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    ...

admin.site.register(Users, UsersAdmin)
