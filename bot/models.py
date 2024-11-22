from django.db import models


class BotMessages(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, default="None")
    message = models.TextField(max_length=3000, blank=False, default="None")

    class Meta:
        verbose_name = "Bot message"
        verbose_name_plural = "Bot messages"

    def __str__(self):
        return self.title
