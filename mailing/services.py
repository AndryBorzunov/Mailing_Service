from django.utils.timezone import now
from django.core.cache import cache
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER, CACHE_ENABLED

from mailing.models import Dispatch, Attempt


def get_mailings_from_cache():
    """Получает список рассылок из кэша, если кэш пуст, получает данные из бд"""

    if not CACHE_ENABLED:
        return Dispatch.objects.all()

    key = "mailing_list"
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Dispatch.objects.all()
    cache.set(key, mailings)
    return mailings


def get_mailings_from_cache_owner(owner):
    """
    Получает список рассылок из кэша, если кэш пуст, получает данные из бд
    Выборка рассылок по хозяину

    """

    if not CACHE_ENABLED:
        return Dispatch.objects.filter(owner=owner)

    key = "mailing_list"
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Dispatch.objects.filter(owner=owner)
    cache.set(key, mailings)
    return mailings


def get_mailing_from_cache(mailing_id):
    """Получает одну рассылку по ключу из кэша"""

    if not CACHE_ENABLED:
        return Dispatch.objects.get(id=mailing_id)

    key = f"mailing_{mailing_id}"
    mailing = cache.get(key)
    if mailing is not None:
        # Проверка актуальности рассылки
        mailing.update_status()
        return mailing

    mailing = Dispatch.objects.get(id=mailing_id)
    # Проверка актуальности рассылки
    mailing.update_status()
    mailing.save()
    cache.set(key, mailing)

    return mailing


def send_mailing(mailing_id):
    """Отправка рассылки"""

    mailing = get_mailing_from_cache(mailing_id)
    attempt = Attempt.objects.create(
        created_at=now(), status="Unsuccessfully", answer="", mailing=mailing
    )
    if mailing.is_active and mailing.status == "Запущена":

        for recipient in mailing.recipients.all():
            try:
                send_mail(
                    subject=mailing.message.theme,
                    message=mailing.message.body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[recipient],
                    fail_silently=False,
                )

                attempt.status = "Successfully"
                attempt.save()
            except Exception as e:
                attempt.status = "Unsuccessfully"
                attempt.answer = str(e)
                attempt.save()
                print(f"Ошибка отправки: {e}")
                raise e

    else:
        if not mailing.is_active:
            # print("Рассылка приостановлена")
            attempt.status = "Unsuccessfully"
            attempt.answer = "Рассылка приостановлена"
            attempt.save()
            raise Exception("Рассылка приостановлена")
        else:
            # print(f"Рассылка {mailing.status}")
            attempt.status = "Unsuccessfully"
            attempt.answer = f"Рассылка {mailing.status}"
            attempt.save()
            raise Exception(f"Рассылка {mailing.status}")
