import csv
from io import TextIOWrapper

from asgiref.sync import async_to_sync
from django import forms
from django.contrib import admin

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


class UsersAdmin(admin.ModelAdmin): ...


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
        required_placeholders = ["refferal_link", "referrals_count", "user_points"]
        missing_placeholders = [ph for ph in required_placeholders if f"{{{ph}}}" not in message]
        if missing_placeholders:
            raise forms.ValidationError(
                f"Сообщение должно содержать следующие плейсхолдеры: {', '.join(missing_placeholders)}."
            )
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
admin.site.register(Addresses, AddressAdmin)
admin.site.register(PointCoefficients, PointCoefficientsAdmin)
admin.site.register(Mailings, MailingsAdmin)
admin.site.register(Airdrops, AirdropsAdmin)
