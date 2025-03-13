from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must give an email address")

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", max_length=128, unique=True)
    first_name = models.CharField(
        verbose_name="First name",
        max_length=40,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name="Last name",
        max_length=40,
        blank=True,
        null=True
    )
    is_staff = models.BooleanField(default=False,)

    objects = UserManager()

    USERNAME_FIELD = "email"
