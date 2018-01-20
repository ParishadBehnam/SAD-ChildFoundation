# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from active_user import forms
from active_user import models
from django.contrib.auth import authenticate, login


@csrf_exempt
def hamyar_register(request):
    form = forms.hamyar_form()
    if request.method == 'GET':
        return render(request, 'hamyar/hamyar_register.html', {'form' : form})
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

            return  HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'hamyar/hamyar_register.html', {'form': form})

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
        print(type)

        table_type = [models.madadjoo, models.madadkar, models.hamyar]
        if user is not None:
            target_username = models.active_user.objects.get(username=username)

            try:
                final_user = table_type[int(type)-2].objects.get(username = target_username)
                login(request, user)
                return HttpResponseRedirect(reverse("general_information"))

            except table_type[int(type)-2].DoesNotExist:
                return render(request, 'login.html', {'form': form})  # TODO
        else:
            return render(request, 'login.html', {'form': form}) #TODO



def general_information(request):
    return render(request, 'general_information.html')


# Create your views here.