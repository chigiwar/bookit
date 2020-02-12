from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    group = models.CharField(
        max_length=7,
        choices=(('user', 'user'), ('manager', 'manager'), ('admin', 'admin'))
    )
    vip = models.BooleanField(default=False)
