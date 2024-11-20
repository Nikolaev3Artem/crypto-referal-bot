from asgiref.sync import async_to_sync
from django.contrib import admin

from backend.models import Addresses, Mailings, PointCoefficients, Users
from backend.services.mailing_service import MailingService


# Register your models here.
class UsersAdmin(admin.ModelAdmin): ...


class AddressAdmin(admin.ModelAdmin): ...


class PointCoefficientsAdmin(admin.ModelAdmin): ...


class MailingsAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "send")
    list_filter = ("send",)
    filter_horizontal = ("users",)

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели.
        Если поле `send` изменилось с False на True, инициируем рассылку.
        """
        send_now = False
        if change:
            # Получаем старый объект из базы данных
            old_obj = Mailings.objects.get(pk=obj.pk)
            if not old_obj.send and obj.send:
                send_now = True
        else:
            # Если создаётся новый объект и `send` установлено в True
            if obj.send:
                send_now = True

        super().save_model(request, obj, form, change)  # Сохраняем объект сначала

        if send_now:
            try:
                # Инициализируем сервис
                mailing_service = MailingService()

                # Используем async_to_sync для вызова асинхронной функции
                async_to_sync(mailing_service.send_mailing)(obj)

                self.message_user(request, "Рассылка отправлена успешно.")
            except Exception as e:
                print(f"Ошибка при отправке рассылки: {e}")
                self.message_user(request, f"Ошибка при отправке рассылки: {e}", level="error")


admin.site.register(Users, UsersAdmin)
admin.site.register(Addresses, AddressAdmin)
admin.site.register(PointCoefficients, PointCoefficientsAdmin)
admin.site.register(Mailings, MailingsAdmin)
