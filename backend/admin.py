from asgiref.sync import async_to_sync
from django import forms
from django.contrib import admin

from backend.constants.enums import BlockchainEnum
from backend.models import Addresses, Mailings, PointCoefficients, Users
from backend.services.mailing_service import MailingService


# Register your models here.
class UsersAdmin(admin.ModelAdmin): ...


class AddressAdmin(admin.ModelAdmin): ...


class PointCoefficientsAdmin(admin.ModelAdmin): ...


class MailingsForm(forms.ModelForm):
    blockchain = forms.ChoiceField(
        choices=[(choice.value, choice.label) for choice in BlockchainEnum],  # Отображаем label для корректности
        required=True,
        label="Блокчейн",
    )

    class Meta:
        model = Mailings
        fields = ["message", "send"]  # Поля модели, которые доступны для редактирования


class MailingsAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "send")
    list_filter = ("send",)
    form = MailingsForm  # Используем кастомную форму

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели.
        Если указан блокчейн, автоматически выбираем пользователей.
        """
        blockchain = form.cleaned_data.get("blockchain")

        # Сначала сохраняем объект, чтобы он получил ID
        super().save_model(request, obj, form, change)

        if blockchain:
            # Фильтруем пользователей с адресами, связанными с указанным блокчейном
            users = Users.objects.filter(
                user__blockchain=blockchain  # `user` связано через ForeignKey в Addresses
            ).distinct()

            # Устанавливаем пользователей после сохранения объекта
            obj.users.set(users)

        if obj.send:
            self.initiate_mailing(request, obj)

    def initiate_mailing(self, request, obj):
        """
        Инициирует рассылку, если она отмечена как отправленная.
        """
        try:
            mailing_service = MailingService()
            async_to_sync(mailing_service.send_mailing)(obj)
            self.message_user(request, "Рассылка отправлена успешно.")
        except Exception as e:
            print(f"Ошибка при отправке рассылки: {e}")
            self.message_user(request, f"Ошибка при отправке рассылки: {e}", level="error")


admin.site.register(Users, UsersAdmin)
admin.site.register(Addresses, AddressAdmin)
admin.site.register(PointCoefficients, PointCoefficientsAdmin)
admin.site.register(Mailings, MailingsAdmin)
