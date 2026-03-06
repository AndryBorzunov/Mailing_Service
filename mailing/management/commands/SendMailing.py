from django.core.management import BaseCommand

from mailing.services import send_mailing


class Command(BaseCommand):
    help = "Запускает рассылку"

    def add_arguments(self, parser):
        # Позиционный аргумент
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        send_mailing(mailing_id)
