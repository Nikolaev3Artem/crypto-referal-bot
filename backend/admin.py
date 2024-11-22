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
from backend.services.user_service import UserService


def parse_user_ids_from_csv(file):
    user_ids = []
    try:
        file = TextIOWrapper(file.file, encoding="utf-8")
        sample = file.read(1024)
        file.seek(0)

        # Определяем разделитель
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample, delimiters=";,")
        has_header = sniffer.has_header(sample)

        reader = csv.reader(file, dialect)

        if has_header:
            next(reader, None)

        for row in reader:
            if row:
                user_id_str = row[0].strip()
                try:
                    user_id = int(user_id_str)
                    user_ids.append(user_id)
                except ValueError:
                    for item in row:
                        item = item.strip()
                        try:
                            user_id = int(item)
                            user_ids.append(user_id)
                            break
                        except ValueError:
                            continue
    except Exception as e:
        print(f"Ошибка при обработке CSV-файла: {e}")

    return Users.objects.filter(user_id__in=user_ids).distinct()


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


class AddressesAdmin(admin.ModelAdmin):
    list_display = ("id", "address", "owner_id", "balance", "blockchain")
    actions = ["export_addresses_to_csv"]

    def export_addresses_to_csv(self, request, queryset):
        """
        Export selected addresses to a CSV file with a semicolon separator.
        """
        field_names = ["id", "address", "owner_id", "balance", "blockchain"]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="addresses.csv"'

        writer = csv.writer(response, delimiter=";")
        writer.writerow(field_names)
        for address in queryset:
            writer.writerow(
                [
                    address.id,
                    address.address,
                    address.owner_id.user_id,
                    address.balance,
                    address.blockchain,
                ]
            )
        return response

    export_addresses_to_csv.short_description = "Export selected addresses to CSV"


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
    message = forms.CharField(
        widget=forms.Textarea,
        label="Сообщение для рассылки",
        help_text="Введите сообщение для рассылки. Используйте ключевые слова: {refferal_link}, {referrals_count}, {user_points}.",
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
        message_template = form.cleaned_data.get("message")

        super().save_model(request, obj, form, change)

        users = Users.objects.none()
        if all_users:
            users = Users.objects.all()
        elif user_ids_file:
            users = parse_user_ids_from_csv(user_ids_file)
        elif blockchains:
            users = Users.objects.filter(user__blockchain__in=blockchains).distinct()
        else:
            users = Users.objects.none()

        obj.users.set(users)

        if obj.send:
            try:
                mailing_service = MailingService()
                for user in users:
                    refferal_link = async_to_sync(UserService.get_refferal_link)(user_id=user.user_id)
                    referrals_count = async_to_sync(UserService.get_user_refferals_count)(user_id=user.user_id)
                    user_points = async_to_sync(UserService.get_user_points)(user_id=user.user_id)

                    context = {
                        "refferal_link": refferal_link,
                        "referrals_count": referrals_count,
                        "user_points": user_points,
                        "username": user.username,
                    }

                    try:
                        formatted_message = message_template.format(**context)
                    except KeyError as ke:
                        formatted_message = f"Ошибка форматирования сообщения: отсутствует ключ {ke}"
                        print(formatted_message)

                    mailing = Mailings(message=formatted_message, send=True)
                    mailing.save()
                    mailing.users.set([user])

                    async_to_sync(mailing_service.send_mailing)(mailing)

                self.message_user(request, "Рассылка успешно отправлена.")
            except Exception as e:
                print(f"Ошибка при отправке рассылки: {e}")
                self.message_user(request, f"Ошибка при отправке рассылки: {e}", level="error")


class AirdropsForm(forms.ModelForm):
    user_ids_file = forms.FileField(
        required=True,
        label="CSV-файл с user_id",
        help_text="Загрузите CSV-файл, содержащий user_id (один ID на строку).",
    )
    message = forms.CharField(
        widget=forms.Textarea,
        label="Сообщение для аирдропа",
        help_text="Введите сообщение для аирдропа. Используйте ключевые слова: {refferal_link}, {referrals_count}, {user_points}.",
    )

    class Meta:
        model = Airdrops
        fields = ["points", "message"]

    def clean_message(self):
        message = self.cleaned_data.get("message")
        return message


class AirdropsAdmin(admin.ModelAdmin):
    list_display = ("id", "points")
    form = AirdropsForm

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели.
        Используем CSV-файл для выдачи поинтов указанным пользователям.
        Также отправляем уведомление о получении аирдропа.
        """
        user_ids_file = form.cleaned_data.get("user_ids_file")
        points = form.cleaned_data.get("points")
        message_template = form.cleaned_data.get("message")

        super().save_model(request, obj, form, change)

        users = Users.objects.none()
        if user_ids_file:
            users = parse_user_ids_from_csv(user_ids_file)

            for user in users:
                user.points += points
                user.save()

            obj.users.set(users)

        if users.exists():
            try:
                mailing_service = MailingService()
                for user in users:
                    refferal_link = async_to_sync(UserService.get_refferal_link)(user_id=user.user_id)
                    referrals_count = async_to_sync(UserService.get_user_refferals_count)(user_id=user.user_id)
                    user_points = async_to_sync(UserService.get_user_points)(user_id=user.user_id)

                    context = {
                        "refferal_link": refferal_link,
                        "referrals_count": referrals_count,
                        "user_points": user_points,
                        "username": user.username,
                    }

                    try:
                        formatted_message = message_template.format(**context)
                    except KeyError as ke:
                        formatted_message = f"Ошибка форматирования сообщения: отсутствует ключ {ke}"
                        print(formatted_message)

                    mailing = Mailings(message=formatted_message, send=True)
                    mailing.save()
                    mailing.users.set([user])

                    async_to_sync(mailing_service.send_mailing)(mailing)

                self.message_user(request, "Аирдроп успешно отправлен и уведомления разосланы.")
            except Exception as e:
                print(f"Ошибка при отправке уведомлений о аирдропе: {e}")
                self.message_user(request, f"Ошибка при отправке уведомлений: {e}", level="error")
        else:
            self.message_user(request, "Аирдроп сохранен, но пользователи не найдены для отправки уведомлений.")


admin.site.register(Users, UsersAdmin)
admin.site.register(Addresses, AddressesAdmin)
admin.site.register(PointCoefficients, PointCoefficientsAdmin)
admin.site.register(Mailings, MailingsAdmin)
admin.site.register(Airdrops, AirdropsAdmin)
