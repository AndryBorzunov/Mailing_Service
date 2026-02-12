from telnetlib import STATUS

from django.db import models


STATUS_CHOICES = [
    ("Completed", "Завершена"),
    ("Created", "Создана"),
    ("Started", "Запущена")
]


RESULT_CHOICES = [
    ("Successfully", "Успешно"),
    ("Unsuccessfully", "Неуспешно")
]

class RecipientMail(models.Model):
    email_address = models.EmailField(
        unique=True,
        verbose_name="Email адрес",
        help_text="Введите email адрес",
    )

    name_fio = models.CharField(
        max_length=128,
        verbose_name="Ф.И.О.",
        help_text="Введите фамилию, имя, отчество",
    )

    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Напишите комментарий"
    )


class Message(models.Model):
    theme = models.CharField(
        max_length=64,
        verbose_name="Тема письма",
        help_text="Введите тему письма"
    )

    body = models.TextField(
        verbose_name="Тело письма",
        help_text="Напишите сообщение"
    )


class Dispatch(models.Model):
    start_at = models.DateTimeField(
        verbose_name="Дата и время первой отправки"
    )

    stop_at = models.DateTimeField(
        verbose_name="Дата и время окончания отправки"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Created"
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        verbose_name="Сообщение",
        help_text="Выберите сообщение для рассылки",
        blank=True,
        null=True
    )

    recipients = models.ManyToManyField(RecipientMail)


class Attempt(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Дата и время попытки"
    )

    status = models.CharField(
        max_length=16,
        choices=RESULT_CHOICES,
        default="Unsuccessfully"
    )

    answer = models.TextField(
        verbose_name="Ответ почтового сервера"
    )

    dispatch = models.ForeignKey(
        Dispatch,
        on_delete=models.SET_NULL,
        verbose_name="Рассылка",
        blank=True,
        null=True
    )
