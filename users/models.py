from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_email_verified', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'manager')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('manager', 'Manager'),
    )
    email = models.EmailField(_('email address'), unique=True)
    is_email_verified = models.BooleanField(default=False)  # Флаг подтверждения email
    is_active = models.BooleanField(default=True)  # Для блокировки пользователей
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # Роль пользователя

    # Укажем кастомный менеджер
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Используем email для аутентификации
    REQUIRED_FIELDS = []  # Убираем требование имени пользователя

    # Удалим поле username, так как оно не нужно
    username = None

    def __str__(self):
        return self.email

    def is_manager(self):
        return self.role == 'manager'

    def is_user(self):
        return self.role == 'user'
