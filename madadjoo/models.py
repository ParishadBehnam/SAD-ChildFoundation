# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from active_user.models import active_user
from madadkar.models import madadkar


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



# Create your models here.
