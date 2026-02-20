import datetime

from django.db import models

from users.models import User


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

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

    def __str__(self):
        return self.email_address


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

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.theme


class Dispatch(models.Model):
    start_time = models.DateTimeField(
        verbose_name="Дата и время первой отправки"
    )

    end_time = models.DateTimeField(
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

    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца рассылки", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.status

    def update_status(self):
        current_time = datetime.datetime.now()

        if self.start_time <= current_time <= self.end_time:
            status = STATUS_CHOICES[2]
        elif current_time > self.end_time:
            status = STATUS_CHOICES[0]
        else:
            status = STATUS_CHOICES[1]

        if self.status != status:
            self.status = status


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

    mailing = models.ForeignKey(
        Dispatch,
        on_delete=models.SET_NULL,
        verbose_name="Рассылка",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"

    def __str__(self):
        return self.status
