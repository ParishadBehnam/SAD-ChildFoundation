# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


class information(models.Model):
    history = models.TextField(primary_key=True, verbose_name="تاریخچه")
    chart = models.CharField(max_length=30, verbose_name="چارت سازمانی")
    goals = models.TextField(verbose_name="اهداف")
    activities = models.TextField(verbose_name="فعالیت‌ها")
    supporters = models.TextField(verbose_name="حمایت‌کننده‌ها")

    class Meta:
        verbose_name_plural = _("اطلاعات کلان سامانه")
        verbose_name= _("اطلاع کلان سامانه")




# Create your models here.
