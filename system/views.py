# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.http import Http404
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from active_user import forms
from django import forms as d_forms
from active_user import models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from system.models import information


@csrf_exempt
def hamyar_register(request):
    form = forms.hamyar_form()
    if request.method == 'GET':
        return render(request, 'hamyar/hamyar_register.html', {'form': form})
    else:
        form = forms.hamyar_form(request.POST)

        if form.is_valid():
            new_hamyar = models.hamyar()
            new_hamyar.first_name = form.cleaned_data['first_name']
            new_hamyar.last_name = form.cleaned_data['last_name']
            new_hamyar.id_number = form.cleaned_data['id_number']
            new_hamyar.phone_number = form.cleaned_data['phone_number']
            new_hamyar.address = form.cleaned_data['address']
            new_hamyar.email = form.cleaned_data['email']
            new_hamyar.set_password(form.cleaned_data['password'])
            new_hamyar.username = form.cleaned_data['username']
            new_hamyar.save()

            login(request, new_hamyar)
            return HttpResponseRedirect(reverse("hamyar_panel")+"?success=1")  # this should be hamyar's own page
        else:
            s = 'ثبت نام شما با خطا مواجه شده‌است. دوباره تلاش کنید.'
            return render(request, 'hamyar/hamyar_register.html', {'form': form,
                                                                   'error_message': s})


@csrf_exempt
def sign_in(request):
    form = forms.login_form()
    if request.method == 'GET':
        return render(request, 'login.html', {'form': form})
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        type = request.POST.get("user_type")

        user = authenticate(request, username=username, password=password)

        table_type = [models.hamyar, models.madadjoo, models.madadkar, models.admin_user]
        user_panel = ["hamyar_panel", "madadjoo_panel", "madadkar_panel", "admin_panel"]
        user_type = ["hamyar", "madadjoo", "madadkar", "admin"]

        try:
            in_admin_table = models.admin_user.objects.get(username=username)
            admin_madadkar_flag = True if in_admin_table is not None and type == '3' else False
        except:
            admin_madadkar_flag = False

        if user is not None and not admin_madadkar_flag:
            target_username = models.active_user.objects.get(username=username)

            try:
                final_user = table_type[int(type) - 1].objects.get(username=target_username)
                if type == '2':
                    f = models.madadkar_remove_madadjoo.objects.filter(madadjoo_id=final_user.id)
                    if len(f) == 0:
                        login(request, user)
                        request.session['type'] = user_type[int(type) - 1]
                        return HttpResponseRedirect(reverse(user_panel[int(type) - 1])+'?success=1')
                    else:
                        return render(request, 'login.html', {'form': form, 'error_message': 'این مددجو از سامانه خارج شده‌است.'})
                login(request, user)
                request.session['type'] = user_type[int(type) - 1]
                return HttpResponseRedirect(reverse(user_panel[int(type) - 1])+'?success=1')
            except table_type[int(type) - 1].DoesNotExist:
                s = 'متاسفانه ورود شما موفقیت‌آمیز نبود. دوباره تلاش کنید.'
                return render(request, 'login.html', {'form': form, 'error_message': s})
        else:
            s = 'متاسفانه ورود شما موفقیت‌آمیز نبود. دوباره تلاش کنید.'
            return render(request, 'login.html', {'form': form, 'error_message': s})


def system_logout(request):
    current_user = request.user
    if current_user is not None:
        logout(request)
    return HttpResponseRedirect(reverse('general_information')+'?success=2')


@csrf_exempt
def general_information(request):
    system = information.objects.first()
    if request.GET.get('success') == '2':
        return render(request, 'general_information.html', {'success_message': 'شما با موفقیت از حساب کاربری خود خارج شدید.',
                                                            'system': system})
    return render(request, 'general_information.html', {'system': system})
