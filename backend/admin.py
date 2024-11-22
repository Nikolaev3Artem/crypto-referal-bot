import csv
from io import TextIOWrapper

from asgiref.sync import async_to_sync
from django import forms
from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponse

from backend.constants.enums import BlockchainEnum
from backend.models import Addresses, Airdrops, Mailings, PointCoefficients, Users
from backend.services.mailing_service import MailingService


@admin.action(description="Экспортировать выбранных пользователей в CSV")
def export_users_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="users.csv"'
    writer = csv.writer(response, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(
        [
            "User ID",
            "Username",
            "Referral Link",
            "Points",
            "Language",
            "Bio",
            "Invited By",
            "Referrals Count",  # Новое поле
        ]
    )

    queryset = queryset.annotate(referrals_count=Count("referrals"))

    for user in queryset:
        invited_by = user.invited_by.user_id if user.invited_by else "None"
        writer.writerow(
            [
                user.user_id,
                user.username,
                user.referral_link,
                user.points,
                user.language if user.language else "",
                user.bio if user.bio else "",
                invited_by,
                user.referrals_count,
            ]
        )

    return response


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "username",
        "referral_link",
        "points",
        "language",
        "bio",
        "invited_by",
        "referrals_count_display",
    )
    search_fields = ("username", "user_id")
    list_filter = ("language",)
    actions = [export_users_to_csv]

    def referrals_count_display(self, obj):
        return obj.referrals.count()

    referrals_count_display.short_description = "Referrals Count"


class AddressAdmin(admin.ModelAdmin): ...


class PointCoefficientsAdmin(admin.ModelAdmin): ...


class MailingsForm(forms.ModelForm):
    blockchains = forms.MultipleChoiceField(
        choices=[(choice.value, choice.label) for choice in BlockchainEnum],
        required=False,
        label="Блокчейны",
        widget=forms.CheckboxSelectMultiple,
    )
    all_users = forms.BooleanField(
        required=False,
        label="Выбрать всех пользователей",
        help_text="Если выбрано, то рассылка будет отправлена всем пользователям.",
    )
    user_ids_file = forms.FileField(
        required=False,
        label="CSV-файл с user_id",
        help_text="Загрузите CSV-файл, содержащий user_id (один ID на строку, и в колонку).",
    )

    class Meta:
        model = Mailings
        fields = ["message", "send"]


class MailingsAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "send")
    list_filter = ("send",)
    form = MailingsForm

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели.
        Учитываем блокчейны, всех пользователей и пользователей из CSV.
        """
        blockchains = form.cleaned_data.get("blockchains")
        all_users = form.cleaned_data.get("all_users")
        user_ids_file = form.cleaned_data.get("user_ids_file")

        # Сохраняем объект, чтобы он получил ID
        super().save_model(request, obj, form, change)

        if all_users:
            # Если выбрано "всем", выбираем всех пользователей
            users = Users.objects.all()
        elif user_ids_file:
            # Если загружен CSV-файл, выбираем пользователей по user_id из файла
            users = self.get_users_from_csv(user_ids_file)
        elif blockchains:
            # Если выбраны блокчейны, фильтруем пользователей по ним
            users = Users.objects.filter(user__blockchain__in=blockchains).distinct()
        else:
            # Если ни блокчейны, ни "всем", ни CSV не выбраны, оставляем поле пустым
            users = Users.objects.none()

        # Устанавливаем пользователей после сохранения объекта
        obj.users.set(users)

        if obj.send:
            self.initiate_mailing(request, obj)

    def get_users_from_csv(self, file):
        """
        Читает CSV-файл и возвращает QuerySet пользователей с указанными user_id.
        """
        try:
            user_ids = []
            # Открываем файл с правильной кодировкой
            file = TextIOWrapper(file.file, encoding="utf-8")
            reader = csv.reader(file)
            for row in reader:
                if row:  # Пропускаем пустые строки
                    try:
                        user_ids.append(int(row[0]))
                    except ValueError:
                        continue  # Пропускаем строки с некорректными ID

            # Возвращаем QuerySet пользователей с указанными user_id
            return Users.objects.filter(user_id__in=user_ids).distinct()
        except Exception as e:
            print(f"Ошибка при обработке CSV-файла: {e}")
            return Users.objects.none()

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


class AirdropsForm(forms.ModelForm):
    user_ids_file = forms.FileField(
        required=True,
        label="CSV-файл с user_id",
        help_text="Загрузите CSV-файл, содержащий user_id (один ID на строку).",
    )

    class Meta:
        model = Airdrops
        fields = ["points"]  # Поля модели, которые доступны для редактирования


class AirdropsAdmin(admin.ModelAdmin):
    list_display = ("id", "points")
    form = AirdropsForm

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели.
        Используем CSV-файл для выдачи поинтов указанным пользователям.
        """
        user_ids_file = form.cleaned_data.get("user_ids_file")
        points = form.cleaned_data.get("points")

        # Сохраняем объект, чтобы он получил ID
        super().save_model(request, obj, form, change)

        if user_ids_file:
            # Получаем пользователей из CSV-файла
            users = self.get_users_from_csv(user_ids_file)

            # Добавляем пользователей к airdrop и начисляем им поинты
            for user in users:
                user.points += points
                user.save()

            # Связываем пользователей с текущим airdrop
            obj.users.set(users)

    def get_users_from_csv(self, file):
        """
        Читает CSV-файл и возвращает QuerySet пользователей с указанными user_id.
        """
        try:
            user_ids = []
            # Открываем файл с правильной кодировкой
            file = TextIOWrapper(file.file, encoding="utf-8")
            reader = csv.reader(file)
            for row in reader:
                if row:  # Пропускаем пустые строки
                    try:
                        user_ids.append(int(row[0]))
                    except ValueError:
                        continue  # Пропускаем строки с некорректными ID

            # Возвращаем QuerySet пользователей с указанными user_id
            return Users.objects.filter(user_id__in=user_ids).distinct()
        except Exception as e:
            print(f"Ошибка при обработке CSV-файла: {e}")
            return Users.objects.none()


admin.site.register(Users, UsersAdmin)
admin.site.register(Addresses, AddressAdmin)
admin.site.register(PointCoefficients, PointCoefficientsAdmin)
admin.site.register(Mailings, MailingsAdmin)
admin.site.register(Airdrops, AirdropsAdmin)
