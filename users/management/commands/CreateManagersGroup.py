from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from  django.contrib.contenttypes.models import ContentType
from mailing.models import Dispatch, RecipientMail, Message, Attempt


class Command(BaseCommand):
    help = 'Создаёт группу "Менеджеры" с разрешением блокировки пользователей и рассылок'

    def handle(self, *args, **options):
        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name='Managers')

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Managers" успешно создана!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Managers" уже существует')
            )

        # Список разрешений для менеджеров
        permissions = [
            ('can_stop_dispatch', 'can stop dispatch'),
            ('can_block_user', 'can block user'),
        ]

        # Создаём кастомные разрешения
        content_type = ContentType.objects.get_for_model(Dispatch)

        for codename, name in permissions:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type,
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Разрешение {codename} успешно создано')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Разрешение {codename} уже существует')
                )

        # Назначение разрешения группе
        for codename, name in permissions:
            try:
                permission = Permission.objects.get(
                    codename=codename,
                    content_type=content_type
                )
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Разрешение {codename} не найдено!')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Разрешения успешно назначены группе {group.name}')
        )
