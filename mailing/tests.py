from datetime import datetime

from django.test import TestCase

from users.models import User
from mailing.models import RecipientMail, Message, Dispatch, Attempt


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="andry7a7@gmail.com")
        self.recipient = RecipientMail.objects.create(
            email_address = "bav@ves-com.com",
            name_fio = "Горбуньков Игорь Николаевич",
            owner = self.user
        )
        self.message = Message.objects.create(
            theme = "Тестовое письмо",
            body = "Тело тестового письма",
            owner = self.user
        )
        self.dispatch = Dispatch.objects.create(
            start_time = "2026-08-10T15:40:00",
            end_time = "2026-08-10T21:40:00", #datetime.now().hour + 10,
            #recipients = self.recipient,
            owner = self.user,
        )
        self.attempt = Attempt.objects.create(
            created_at = datetime.now(),
            mailing = self.dispatch
        )

        #self.client.force_authenticate(user=self.user)
        self.client.force_login(user=self.user)

    def test_model_mailing_summary(self):
        # Отправляем get-запрос к представлению
        response = self.client.get('/')

        # Проверяем статус ответа
        self.assertEqual(response.status_code, 200)

    def test_model_mailing_summary_template(self):
        # Проверяем, что для ответа был использован конкретны шаблон
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'mailing/summary.html')

    def test_model_dispatch_detail(self):

        print('Эта рассылка: ' + 'mailing/' + str(self.dispatch.pk) + '/')
        #response = self.client.get('mailing/' + str(self.dispatch.pk) + '/')
        self.client.force_login(user=self.user)
        response = self.client.get('mailings/')
        print(response.request)
        # Проверяем статус ответа
        self.assertEqual(response.status_code, 404)
