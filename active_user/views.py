# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
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

@login_required
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

        invest_percentage = request.POST.get('invest_percentage')
        invest_percentage = '0.0' if invest_percentage == '' else invest_percentage
        description = request.POST.get('description')
        type = request.POST.get('type')
        # corr_madadkar = models.active_user.objects.get(username=request.user)
        corr_madadkar = None
        cash = True if request.POST.get('cash') == 'cash' else False
        urgent = True if request.POST.get('urgent') == 'urgent' else False

        new_madadjoo = models.madadjoo(username=username, first_name=first_name,
                                       last_name=last_name, id_number=id_number, phone_number=phone_number,
                                       address=address, email=email, profile_pic=profile_pic, bio=bio,
                                       edu_status=edu_status, successes=successes, removed=False,
                                       invest_percentage=invest_percentage, corr_madadkar=corr_madadkar, confirmed=True,

                                       )
        new_madadjoo.set_password(request.POST.get("password"))
        try:
            new_madadjoo.save()
            new_req = models.requirements(description=description, type=type, confirmed=True, urgent=urgent,
                                          cash=cash, madadjoo=new_madadjoo)
            new_req.save()
        except IntegrityError:
            return render_to_response("admin/add_a_madadjoo.html",
                                      {"message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError:
            return render_to_response("admin/add_a_madadjoo.html", {"message": "لطفا موارد الزامی را تکمیل کنید"})

        return HttpResponseRedirect(reverse("admin_panel"))

@csrf_exempt
def add_a_madadjoo_madadkar(request):
    if request.method == "GET":
        # print(request.user)
        return render(request, 'madadkar/add_a_madadjoo.html')
    else:
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

        invest_percentage = request.POST.get('invest_percentage')
        invest_percentage = '0.0' if invest_percentage == '' else invest_percentage
        description = request.POST.get('description')
        type = request.POST.get('type')

        id_madadkar = models.active_user.objects.get(username=request.user).id
        corr_madadkar = models.madadkar.objects.get(active_user_ptr_id=id_madadkar)

        cash = True if request.POST.get('cash') == 'cash' else False
        urgent = True if request.POST.get('urgent') == 'urgent' else False

        new_madadjoo = models.madadjoo(username=username, first_name=first_name,
                                       last_name=last_name, id_number=id_number, phone_number=phone_number,
                                       address=address, email=email, profile_pic=profile_pic, bio=bio,
                                       edu_status=edu_status, successes=successes, removed=False,
                                       invest_percentage=invest_percentage, corr_madadkar=corr_madadkar, confirmed=False,

                                       )
        new_madadjoo.set_password(request.POST.get("password"))
        try:
            new_madadjoo.save()
            new_req = models.requirements(description=description, type=type, confirmed=False, urgent=urgent,
                                          cash=cash, madadjoo=new_madadjoo)
            new_req.save()
        except IntegrityError:
            return render_to_response("madadkar/add_a_madadjoo.html",
                                      {"message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError:
            return render_to_response("madadkar/add_a_madadjoo.html", {"message": "لطفا موارد الزامی را تکمیل کنید"})

        return HttpResponseRedirect(reverse("madadkar_panel"))


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
        phone_number = request.POST.get('phone_number')
        phone_number = '0' if phone_number == '' else phone_number
        address = request.POST.get('address')
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
    if request.method == "GET":
        return render(request, 'admin/add_a_hamyar.html')
    else:
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        phone_number = request.POST.get('phone_number', 0)
        phone_number = '0' if phone_number == '' else phone_number
        address = request.POST.get('address')
        email = request.POST.get('email')
        profile_pic = request.POST.get('profile_pic')

        new_madadkar = models.hamyar(username=username, first_name=first_name,
                                     last_name=last_name, id_number=id_number, phone_number=phone_number,
                                     address=address, email=email, profile_pic=profile_pic)
        new_madadkar.set_password(request.POST.get("password"))
        try:
            new_madadkar.save()
        except IntegrityError:
            return render_to_response("admin/add_a_hamyar.html",
                                      {"message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError:
            return render_to_response("admin/add_a_hamyar.html", {"message": "لطفا موارد الزامی را تکمیل کنید"})

        return HttpResponseRedirect(reverse("admin_panel"))


def payment_reports_admin(request):
    return render(request, 'admin/payment_reports.html')


def activity_report(request):
    return render(request, 'admin/activity_reports.html')


def madadjoo_paid_report(request):
    return render(request, 'admin/madadjoo_paid_report.html')
