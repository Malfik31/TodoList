from django.conf import settings
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    is_done = models.BooleanField("Выполнено", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ["is_done", "-created_at"]
        verbose_name = "задача"
        verbose_name_plural = "задачи"

    def __str__(self):
        return self.title
