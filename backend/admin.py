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
    blockchains = forms.MultipleChoiceField(
        choices=[(choice.value, choice.label) for choice in BlockchainEnum],
        required=False,
        label="Блокчейны",
        widget=forms.CheckboxSelectMultiple,  # Используем чекбоксы для выбора нескольких блокчейнов
    )
    all_users = forms.BooleanField(
        required=False,
        label="Выбрать всех пользователей",
        help_text="Если выбрано, то рассылка будет отправлена всем пользователям.",
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
        Если указаны блокчейны или выбран флаг "всем", выбираем соответствующих пользователей.
        """
        blockchains = form.cleaned_data.get("blockchains")
        all_users = form.cleaned_data.get("all_users")

        # Сохраняем объект, чтобы он получил ID
        super().save_model(request, obj, form, change)

        if all_users:
            # Если выбрано "всем", выбираем всех пользователей
            users = Users.objects.all()
        elif blockchains:
            # Если выбраны блокчейны, фильтруем пользователей по ним
            users = Users.objects.filter(user__blockchain__in=blockchains).distinct()
        else:
            # Если ни блокчейны, ни "всем" не выбраны, оставляем поле пустым
            users = Users.objects.none()

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
