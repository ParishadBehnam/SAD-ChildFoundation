# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser

from system.models import information
from django.utils.translation import ugettext_lazy as _


class active_user(AbstractUser):
    AbstractUser._meta.get_field('username').verbose_name = "نام کاربری"
    AbstractUser._meta.get_field('password').verbose_name = "کلمه عبور"

    first_name = models.CharField(max_length=100, null=True, verbose_name="نام")
    last_name = models.CharField(max_length=100, null=True, verbose_name="نام خانوادگی")
    id_number = models.IntegerField(unique=True, null=False, verbose_name="کد ملی")
    phone_number = models.IntegerField(null=True, verbose_name="شماره تلفن")
    address = models.TextField(null=True, verbose_name="آدرس")
    profile_pic = models.ImageField(null=True, verbose_name="تصویر")
    email = models.EmailField(blank=True, max_length=254, verbose_name='رایانامه')

    def save(self, *args, **kwargs):
        return super(active_user, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("کاربران فعال")
        verbose_name = _("کاربر فعال")

    def is_admin(self):
        try:
            admin_user.objects.get(username=self.username)
            return True
        except:
            return False

    def is_hamyar(self):
        try:
            hamyar.objects.get(username=self.username)
            return True
        except:
            return False

    def is_madadkar(self):
        try:
            madadkar.objects.get(username=self.username)
            try:
                admin_user.objects.get(username=self.username)
                return False
            except:
                return True
        except:
            return False

    def is_madadjoo(self):
        try:
            madadjoo.objects.get(username=self.username)
            return True
        except:
            return False


class madadkar(active_user):
    bio = models.TextField(null=True, verbose_name="شرح حال")

    class Meta:
        verbose_name_plural = _("مددکاران")
        verbose_name = _("مددکار")


class admin_user(madadkar):
    class Meta:
        verbose_name_plural = _("مدیران")
        verbose_name = _("مدیر")


class hamyar(active_user):
    class Meta:
        verbose_name_plural = _("همیاران")
        verbose_name = _("همیار")


class madadjoo(active_user):
    bio = models.TextField(null=True, verbose_name="شرح حال")
    edu_status = models.TextField(null=True, verbose_name="وضعیت تحصیلی")
    successes = models.TextField(null=True, verbose_name="شرح موفقیت‌ها")
    confirmed = models.BooleanField(default=False, verbose_name="تایید شده")
    removed = models.BooleanField(default=False, verbose_name="حذف شده")
    invest_percentage = models.FloatField(default=0.0, null=True, verbose_name="درصد پس‌انداز")
    corr_madadkar = models.ForeignKey(madadkar, null=True, on_delete=models.CASCADE, verbose_name="مددجوی حمایت‌کننده")

    class Meta:
        verbose_name_plural = _("مددجویان")
        verbose_name = _("مددجو")


class madadkar_remove_madadjoo(models.Model):
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE, null=True)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE, unique=True)
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)


class madadjoo_madadkar_letter(models.Model):
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE)
    text = models.TextField()
    title = models.TextField(default='')
    date = models.DateTimeField(auto_now=True)
    thank = models.BooleanField(null=False, default=False)

    class Meta:
        unique_together = (("madadjoo", "date"),)


class requirements(models.Model):
    description = models.TextField()
    type = models.CharField(choices=(('mo', 'monthly'), ('ann', 'annual'), ('inst', 'instantly')), null=True,
                            max_length=60)
    confirmed = models.BooleanField(default=True)
    urgent = models.BooleanField(default=False)
    cash = models.BooleanField(default=True)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)


class hamyar_system_payment(models.Model):
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    system = models.ForeignKey(information, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("hamyar", "date"),)


class sponsership(models.Model):
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("madadjoo", "hamyar"),)


class hamyar_madadjoo_payment(models.Model):
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    need = models.ForeignKey(requirements, on_delete=models.CASCADE)
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    type = models.CharField(choices=(('mo', 'monthly'), ('ann', 'annual'), ('inst', 'instantly')), max_length=60)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("madadjoo", "hamyar", "date"),)


class hamyar_madadjoo_non_cash(models.Model):
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()

    class Meta:
        unique_together = (("hamyar", "date", "madadjoo"),)


class hamyar_madadjoo_meeting(models.Model):  # should process this table when madadkar wants to see her letters
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("hamyar", "date", "madadjoo"),)


class madadjoo_hamyar_letter(models.Model):
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    title = models.TextField(default="")
    confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("hamyar", "date", "madadjoo"),)


class add_madadjoo_admin_letter(models.Model):
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    date = models.DateTimeField(auto_now=True)


class urgent_need_admin_letter(models.Model):
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE)
    need = models.ForeignKey(requirements, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class warning_admin_letter(models.Model):
    admin_user = models.ForeignKey(admin_user, on_delete=models.CASCADE, related_name='sender')
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE, related_name='receiver')
    date = models.DateTimeField(auto_now=True)


class substitute_a_madadjoo(models.Model):
    remove = models.ForeignKey(madadkar_remove_madadjoo, on_delete=models.CASCADE)
    substituted_madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("remove", "substituted_madadjoo"),)

class request_for_change_madadkar(models.Model):
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("madadjoo", "date"),)


class admin_madadjoo_payment(models.Model):
    admin = models.ForeignKey(admin_user, on_delete=models.CASCADE)
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    need = models.ForeignKey(requirements, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    type = models.CharField(choices=(('mo', 'monthly'), ('ann', 'annual'), ('inst', 'instantly')), max_length=60)

    class Meta:
        unique_together = (("madadjoo", "admin", "date"),)
