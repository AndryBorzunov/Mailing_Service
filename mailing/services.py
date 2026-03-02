from django.utils.timezone import now
from django.core.cache import cache
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER, CACHE_ENABLED

from mailing.models import Dispatch, Attempt

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
    #print(mailing.status)
    attempt = Attempt.objects.create(created_at=now(), status="Unsuccessfully", answer="",
                                     mailing=mailing)
    if mailing.is_active and mailing.status == "Запущена":

        for recipient in mailing.recipients.all():

            try:
                send_mail(
                    subject=mailing.message.theme,
                    message=mailing.message.body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[recipient],
                    fail_silently=False
                )

                attempt.status = "Successfully"
                attempt.save()
            except Exception as e:
                attempt.status = "Unsuccessfully"
                attempt.answer = str(e)
                print(f"Ошибка отправки: {e}")
                raise e

    else:
        if not mailing.is_active:
            #print("Рассылка приостановлена")
            attempt.status = "Unsuccessfully"
            attempt.answer = "Рассылка приостановлена"
            attempt.save()
            raise Exception("Рассылка приостановлена")
        else:
            #print(f"Рассылка {mailing.status}")
            attempt.status = "Unsuccessfully"
            attempt.answer = f"Рассылка {mailing.status}"
            attempt.save()
            raise Exception(f"Рассылка {mailing.status}")
