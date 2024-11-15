from django.db import models


class BotMessages(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, null=False, default="")
    message = models.CharField(max_length=3000, blank=False, null=False, default="")

    class Meta:
        verbose_name = "Message to bot"
        verbose_name_plural = "Messages to bot"

    def __str__(self):
        return self.title
