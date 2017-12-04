# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser


class active_user(AbstractUser):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    id_number = models.IntegerField(unique=True, null=False)
    phone_number = models.IntegerField(null=True)
    address = models.TextField(null=True)
