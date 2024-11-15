from django.contrib import admin

from .models import BotMessages


# Register your models here.
@admin.register(BotMessages)
class BotMessagesAdmin(admin.ModelAdmin):
    fields = ["title", "message"]
