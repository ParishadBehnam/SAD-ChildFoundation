# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class information(models.Model):
    history = models.TextField(primary_key=True)
    chart = models.CharField(max_length=30)
    goals = models.TextField()
    activities = models.TextField()
    supporters = models.TextField()




# Create your models here.
