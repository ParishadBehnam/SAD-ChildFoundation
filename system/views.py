# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import Http404
from django.shortcuts import render


def show_madadjoo(request):
    return render(request, 'show_madadjoo.html')

def general_information(request):
    return render(request, 'general_information.html')


# Create your views here.