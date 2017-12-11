# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import Http404
from django.shortcuts import render


def show_madadjoo(request):
    return render(request, 'show_madadjoo.html')

def hamyar_register(request):
    return render(request, 'hamyar_register.html')

def login(request):
    return render(request, 'login.html')

def general_information(request):
    return render(request, 'general_information.html')


# Create your views here.