from django.utils.timezone import now
from django.core.cache import cache
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER, CACHE_ENABLED

from mailing.models import Dispatch, STATUS_CHOICES, Attempt, RESULT_CHOICES

def send_mailing(mailing_id):
    mailing = None
    if not CACHE_ENABLED:
        mailing = Dispatch.objects.get(id=mailing_id)

    # Работа с кешем
    key = f"mailing_{mailing_id}"
    mailing = cache.get(key)
    if mailing is None:
        mailing = Dispatch.objects.get(id=mailing_id)
        cache.set(key, mailing)

    # Проверка актуальности рассылки
    mailing.update_status()
    print(mailing.status)
    if mailing.is_active and mailing.status == "Запущена":
        recipient_list = []
        for recipient in mailing.recipients.all():
            recipient_list.append(recipient)

        try:
            result = send_mail(
                subject=mailing.message.theme,
                message=mailing.message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False
            )
            attempt = Attempt.objects.create(created_at=now(), status="Successfully", answer="",
                                             mailing=mailing)
            attempt.status = "Successfully"
            print(f"Отправка ОК: {result} из {len(recipient_list)}")
        except Exception as e:
            attempt = Attempt.objects.create(created_at=now(), status="Unsuccessfully", answer=str(e),
                                             mailing=mailing)
            print(f"Ошибка отправки: {e}")

    else:
        if not mailing.is_active:
            print("Рассылка приостановлена")
        else:
            print(f"Рассылка {mailing.status}")
