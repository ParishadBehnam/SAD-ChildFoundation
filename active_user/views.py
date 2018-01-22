# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from active_user import forms
from active_user import models


# Create your views here.

def home_madadkar(request):
    return render(request, 'madadkar/home_madadkar.html')

def home_hamyar(request):
    return render(request, 'hamyar/home_hamyar.html')

def home_madadjoo(request):
    return render(request, 'madadjoo/home_madadjoo.html')

def home_admin(request):
    return render(request, 'admin/home_admin.html')

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


def show_hamyar_information(request):
    return render(request, 'hamyar/show_details.html')


def edit_hamyar_information(request):
    return render(request, 'hamyar/edit_details.html')


@csrf_exempt
def edit_hamyar_information(request):
    form = forms.hamyar_form()
    if request.method == 'GET':
        return render(request, 'hamyar/hamyar_register.html', {'form': form})
    else:
        form = forms.hamyar_form(request.POST)

        if form.is_valid():

            # new_hamyar.first_name = form.cleaned_data['first_name']
            # new_hamyar.last_name = form.cleaned_data['last_name']
            # new_hamyar.id_number = form.cleaned_data['id_number']
            # new_hamyar.phone_number = form.cleaned_data['phone_number']
            # new_hamyar.address = form.cleaned_data['address']
            # new_hamyar.email = form.cleaned_data['email']
            # new_hamyar.set_password(form.cleaned_data['password'])
            # new_hamyar.username = form.cleaned_data['username']
            # new_hamyar.save()
            #
            # login(request, new_hamyar)
            return HttpResponseRedirect(reverse("hamyar_panel"))  # this should be hamyar's own page
        else:
            return render(request, 'hamyar/hamyar_register.html', {'form': form})


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
    if request.method == "GET":
        return render(request, 'admin/add_a_madadjoo.html')
    else:
        print('hiiii')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        phone_number = request.POST.get('phone_number')
        phone_number = '0' if phone_number == '' else phone_number
        address = request.POST.get('addres')
        email = request.POST.get('email')
        profile_pic = request.POST.get('profile_pic')
        bio = request.POST.get('bio')
        edu_status = request.POST.get('edu_status')
        successes = request.POST.get('successes')
        confirmed = request.POST.get('confirmed')
        removed = request.POST.get('removed')
        invest_percentage = request.POST.get('invest_percentage')
        invest_percentage = '0.0' if invest_percentage == '' else invest_percentage
        description = request.POST.get('description')
        type = request.POST.get('type')
        # corr_madadkar = models.active_user.objects.get(username=request.user)
        corr_madadkar = None

        print(request.POST.get('type'))
        print(invest_percentage)
        print(phone_number)


        new_madadkar = models.madadjoo(username=username, first_name=first_name,
                                       last_name=last_name, id_number=id_number, phone_number=phone_number,
                                       address=address, email=email, profile_pic=profile_pic, bio=bio,
                                       edu_status=edu_status, successes=successes, removed=False,
                                       invest_percentage=invest_percentage, corr_madadkar=corr_madadkar, confirmed=True,
                                        )
        new_madadkar.set_password(request.POST.get("password"))
        try:
            new_madadkar.save()
            print("saved")
        except IntegrityError:
            print("error1")
            return render_to_response("admin/add_a_madadjoo.html",
                                      {"message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError as e:
            print(e)
            return render_to_response("admin/add_a_madadjoo.html", {"message": "لطفا موارد الزامی را تکمیل کنید"})

        return HttpResponseRedirect(reverse("admin_panel"))


def show_madadkar_admin(request):
    return render(request, 'admin/show_madadkar.html')


def show_a_madadkar_admin(request):
    return render(request, 'admin/show_a_madadkar.html')


def edit_a_madadkar_admin(request):
    return render(request, 'admin/edit_a_madadkar.html')


def add_a_madadkar_admin(request):
    if request.method == "GET":
        return render(request, 'admin/add_a_madadkar.html')
    else:
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        phone_number = request.POST.get('phone_number', 0)
        address = request.POST.get('addres')
        email = request.POST.get('email')
        profile_pic = request.POST.get('profile_pic')
        bio = request.POST.get('bio')

        new_madadkar = models.madadkar(username=username, first_name=first_name,
                                       last_name=last_name, id_number=id_number, phone_number=phone_number,
                                       address=address, email=email, profile_pic=profile_pic, bio=bio)
        new_madadkar.set_password(request.POST.get("password"))
        try:
            new_madadkar.save()
        except IntegrityError:
            return render_to_response("admin/add_a_madadkar.html",
                                      {"message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError:
            return render_to_response("admin/add_a_madadkar.html", {"message": "لطفا موارد الزامی را تکمیل کنید"})

        return HttpResponseRedirect(reverse("admin_panel"))


def show_hamyar_admin(request):
    return render(request, 'admin/show_hamyar.html')


def show_a_hamyar_admin(request):
    return render(request, 'admin/show_a_hamyar.html')


def edit_a_hamyar_admin(request):
    return render(request, 'admin/edit_a_hamyar.html')


def add_a_hamyar_admin(request):
    return render(request, 'admin/add_a_hamyar.html')


def payment_reports_admin(request):
    return render(request, 'admin/payment_reports.html')


def activity_report(request):
    return render(request, 'admin/activity_reports.html')


def madadjoo_paid_report(request):
    return render(request, 'admin/madadjoo_paid_report.html')
