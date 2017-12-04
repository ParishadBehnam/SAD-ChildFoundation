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


class madadjoo(active_user):
    bio = models.TextField(null=True)
    edu_status = models.TextField(null=True)
    successes = models.TextField(null=True)
    confirmed = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    invest_percentage = models.FloatField(default=0.0, null=True)
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE)


class madadjoo_madadkar_letter():
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (("madadjoo", "date"),)


class requirements():
    description = models.TextField(null=True)
    type = models.CharField(choices=['monthly', 'annual', 'instantly'], max_length=60)
    confirmed = models.BooleanField(default=False)
    urgent = models.BooleanField(default=False)
    cash = models.BooleanField(default=True)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)

class hamyar(active_user):
    pass

class hamyar_system_payment():
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    system = models.ForeignKey(information, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (("hamyar", "date"),)


class sponsership():
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("madadjoo", "madadkar"),)

class hamyar_madadjoo_payment():
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    type = models.CharField(choices=['monthly', 'annual', 'instantly'], max_length=60)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (("madadjoo", "hamyar", "date"),)


class hamyar_madadjoo_non_cash():
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    text = models.TextField()

    class Meta:
        unique_together = (("hamyar", "date", "madadjoo"),)


class hamyar_madadjoo_meeting(): #should process this table when madadkar wants to see her letters
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (("hamyar", "date", "madadjoo"),)

class madadjoo_hamyar_letter():
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    text = models.TextField()
    confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("hamyar", "date", "madadjoo"),)

class madadkar(active_user):
    bio = models.TextField(null=True)

class madadkar_remove_madadjoo():
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE, unique=True)
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField()
