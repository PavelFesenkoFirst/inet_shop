
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, phone, password, is_staff, is_superuser,
                     **extra_fields):
        user = self.model(
            email=email, phone=phone, is_staff=is_staff,
            is_superuser=is_superuser, date_joined=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # метод для быстрого создания пользователя (User.objects.create_user())
    def create_user(self, email, phone, password, **extra_fields):
        return self._create_user(
            email, phone, password, False, False, **extra_fields
        )

    # метод, который использует команда python manage.py createsuperuser
    def create_superuser(self, email, phone, password, **extra_fields):
        return self._create_user(
            email, phone, password, True, True, **extra_fields
        )
