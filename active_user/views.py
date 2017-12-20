# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def show_madadjoo(request):
    return render(request, 'madadkar/show_madadjoo.html')

def show_madadjoo_hamyar(request):
    return render(request, 'hamyar/show_madadjoo.html')

def edit_madadjoo(request):
    return render(request, 'madadkar/edit_madadjoo.html')

def add_madadjoo(request):
    return render(request, 'madadkar/add_madadjoo.html')

def show_a_madadjoo(request):
    return render(request, 'madadkar/show_a_madadjoo.html')

def show_a_madadjoo_hamyar(request):
    return render(request, 'hamyar/show_a_madadjoo.html')

def show_a_hamyar(request):
    return render(request, 'madadkar/show_a_hamyar.html')

def send_letter(request):
    return render(request, 'madadkar/send_letter.html')

def send_letter_hamyar(request):
    return render(request, 'hamyar/send_letter.html')

def inbox(request):
    return render(request, 'madadkar/inbox.html')

def inbox_hamyar(request):
    return render(request, 'hamyar/inbox.html')

def madadkar_panel(request):
    return render(request, 'madadkar/madadkar_panel.html')

def hamyar_panel(request):
    return render(request, 'hamyar/hamyar_panel.html')

def payment_reports(request):
    return render(request, 'hamyar/payment_reports.html')

def select_madadjoo(request):
    return render(request, 'hamyar/select_madadjoo.html')

def show_madadjoo_report(request):
    return render(request, 'hamyar/madadjoo_report.html')

def madadjoo_panel(request):
    return render(request, 'madadjoo/madadjoo_panel.html')

def show_hamyar(request):
    return render(request, 'madadjoo/show_hamyar.html')

def show_a_madadkar_madadjoo(request):
    return render(request, 'madadjoo/show_a_madadkar.html')

def show_a_hamyar_madadjoo(request):
    return render(request, 'madadjoo/show_a_hamyar.html')

def payment_reports_madadjoo(request):
    return render(request, 'madadjoo/payment_reports.html')

def send_letter_hamyar_madadjoo(request):
    return render(request, 'madadjoo/send_letter_hamyar.html')

def send_request_madadkar(request):
    return render(request, 'madadjoo/send_request_madadkar.html')

def send_gratitude_letter(request):
    return render(request, 'madadjoo/send_gratitude_letter.html')

def show_madadjoo_information(request):
    return render(request, 'madadjoo/show_madadjoo_information.html')

def admin_panel(request):
    return render(request, 'admin/admin_panel.html')

def show_madadjoo_admin(request):
    return render(request, 'admin/show_madadjoo.html')

def show_a_madadjoo_admin(request):
    return render(request, 'admin/show_a_madadjoo.html')

def edit_a_madadjoo_admin(request):
    return render(request, 'admin/edit_a_madadjoo.html')

def inbox_admin(request):
    return render(request, 'admin/inbox.html')

def add_a_madadjoo_admin(request):
    return render(request, 'admin/add_a_madadjoo.html')

def show_madadkar_admin(request):
    return render(request, 'admin/show_madadkar.html')

def show_a_madadkar_admin(request):
    return render(request, 'admin/show_a_madadkar.html')

def edit_a_madadkar_admin(request):
    return render(request, 'admin/edit_a_madadkar.html')

def add_a_madadkar_admin(request):
    return render(request, 'admin/add_a_madadkar.html')

def show_hamyar_admin(request):
    return render(request, 'admin/show_hamyar.html')

def show_a_hamyar_admin(request):
    return render(request, 'admin/show_a_hamyar.html')

def edit_a_hamyar_admin(request):
    return render(request, 'admin/edit_a_hamyar.html')

def add_a_hamyar_admin(request):
    return render(request, 'admin/add_a_hamyar.html')



