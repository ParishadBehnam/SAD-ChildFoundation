# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def show_madadjoo(request):
    return render(request, 'show_madadjoo.html')

def edit_madadjoo(request):
    return render(request, 'edit_madadjoo.html')

def add_madadjoo(request):
    return render(request, 'add_madadjoo.html')

def show_a_madadjoo(request):
    return render(request, 'show_a_madadjoo.html')

def show_a_hamyar(request):
    return render(request, 'show_a_hamyar.html')

def send_letter(request):
    return render(request, 'send_letter.html')

def inbox(request):
    return render(request, 'inbox.html')

def madadkar_panel(request):
    return render(request, 'madadkar_panel.html')
