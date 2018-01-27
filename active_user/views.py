# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from active_user import forms
from active_user import models

from active_user.decorators import admin_login_required
from active_user.decorators import madadkar_login_required
from active_user.decorators import hamyar_login_required
from active_user.decorators import madadjoo_login_required
from active_user.models import madadjoo, hamyar, madadkar, sponsership, \
    madadjoo_madadkar_letter, madadjoo_hamyar_letter , hamyar_madadjoo_meeting


@madadkar_login_required
def home_madadkar(request):
    return render(request, 'madadkar/home_madadkar.html')


@hamyar_login_required
def home_hamyar(request):
    return render(request, 'hamyar/home_hamyar.html')


@madadjoo_login_required
def home_madadjoo(request):
    return render(request, 'madadjoo/home_madadjoo.html')


@admin_login_required
def home_admin(request):
    return render(request, 'admin/home_admin.html')


@madadkar_login_required
def show_madadjoo(request):
    all_madadjoo = madadjoo.objects.filter(corr_madadkar=request.user.id)
    return render(request, 'madadkar/show_madadjoo.html', {'madadjoos': all_madadjoo})


@hamyar_login_required
def show_madadjoo_hamyar(request):
    all_madadjoo = madadjoo.objects.filter(sponsership__hamyar_id=request.user.id)
    return render(request, 'hamyar/show_madadjoo.html', {'madadjoos': all_madadjoo})


@madadkar_login_required
def edit_madadjoo(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)

    return render(request, 'madadkar/edit_madadjoo_full.html', {'user': target_madadjoo, 'needs': needs, 'hamyars': hamyars})


@madadkar_login_required
def add_madadjoo(request):
    return render(request, 'madadkar/add_madadjoo.html')


@madadkar_login_required
def show_a_madadjoo(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
    # user = {'first_name': target_madadjoo.first_name,
    #         'last_name': target_madadjoo.last_name,
    #         'id_number': target_madadjoo.id_number,
    #         'phone_number': target_madadjoo.phone_number,
    #         'email': target_madadjoo.email,
    #         'address': target_madadjoo.address,
    #         'profile_pic': target_madadjoo.profile_pic,
    #         'invest': target_madadjoo.invest_percentage,
    #         'successes': target_madadjoo.successes,
    #         'bio': target_madadjoo.bio,
    #         'edu_status': target_madadjoo.edu_status,
    #         'need': {'description': needs.description, 'type': needs.type, 'urgent': needs.urgent, 'cash': needs.cash}
    #         }
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)
    return render(request, 'madadkar/show_a_madadjoo.html',
                  {'user': target_madadjoo, 'needs': needs, 'hamyars': hamyars})


@hamyar_login_required
def support_a_madadjoo(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    target_hamyar = request.user
    new_sponsership = sponsership(hamyar_id=target_hamyar.id, madadjoo_id=target_madadjoo.id)
    new_sponsership.save()

    all_madadjoo = madadjoo.objects.values('username', 'first_name', 'last_name', 'bio')
    return render(request, 'hamyar/select_madadjoo.html',
                  {'madadjoos': list(all_madadjoo), 'message': 'مددجوی مورد نظر تحت حمایت شما قرار گرفت'})


@hamyar_login_required
def show_a_madadjoo_hamyar(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
    # user = {'first_name': target_madadjoo.first_name,
    #         'last_name': target_madadjoo.last_name,
    #         'id_number': target_madadjoo.id_number,
    #         'phone_number': target_madadjoo.phone_number,
    #         'email': target_madadjoo.email,
    #         'address': target_madadjoo.address,
    #         'profile_pic': target_madadjoo.profile_pic,
    #         'invest': target_madadjoo.invest_percentage,
    #         'successes': target_madadjoo.successes,
    #         'bio': target_madadjoo.bio,
    #         'edu_status': target_madadjoo.edu_status,
    #         'need': {'description': needs.description, 'type': needs.type, 'urgent': needs.urgent, 'cash': needs.cash}
    #         }
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)
    return render(request, 'hamyar/show_a_madadjoo.html', {'user': target_madadjoo, 'needs': needs, 'hamyars': hamyars})


@madadkar_login_required
def show_a_hamyar(request):
    target_hamyar = hamyar.objects.get(username=request.GET.get('username', ''))
    madadjoos = madadjoo.objects.filter(corr_madadkar_id=request.user.id, sponsership__hamyar_id=target_hamyar.id)
    return render(request, 'madadkar/show_a_hamyar.html', {'hamyar': target_hamyar, 'madadjoos': madadjoos})


@madadkar_login_required
def send_letter(request):
    return render(request, 'madadkar/send_letter.html')


@hamyar_login_required
def send_letter_hamyar(request):
    return render(request, 'hamyar/send_letter.html')


@madadkar_login_required
def inbox_madadkar(request):
    all_madadjoo_madadkar_letters = \
        madadjoo_madadkar_letter.objects.filter(madadkar_id=request.user.id)
    all_madadjoo_hamyar_letters = \
        madadjoo_hamyar_letter.objects.filter(madadjoo__corr_madadkar=request.user.id, confirmed=0)
    all_hamyar_madadjoo_letters = \
        hamyar_madadjoo_meeting.objects.filter(madadjoo__corr_madadkar=request.user.id)

    return render(request, 'madadkar/inbox.html',
                  {'madadjoo_madadkar_letters': all_madadjoo_madadkar_letters,
                   'madadjoo_hamyar_letters': all_madadjoo_hamyar_letters,
                   'hamyar_madadjoo_letters': all_hamyar_madadjoo_letters})


@madadkar_login_required
def letter_madadjoo_content_madadkar(request):
    target_letter = models.madadjoo_madadkar_letter.objects.get(id=request.GET.get('letter', ''))
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_madadkar = models.madadkar.objects.get(active_user_ptr_id=target_letter.madadkar_id)
    all_madadjoo_madadkar_letters = \
        madadjoo_madadkar_letter.objects.filter(madadkar_id=request.user.id)
    all_madadjoo_hamyar_letters = \
        madadjoo_hamyar_letter.objects.filter(madadjoo__corr_madadkar=request.user.id, confirmed=0)
    all_hamyar_madadjoo_letters = \
        hamyar_madadjoo_meeting.objects.filter(madadjoo__corr_madadkar=request.user.id)
    return render(request, 'madadkar/letter_content_removable.html',
                  {'madadjoo_madadkar_letters': all_madadjoo_madadkar_letters,
                   'madadjoo_hamyar_letters': all_madadjoo_hamyar_letters,
                   'hamyar_madadjoo_letters': all_hamyar_madadjoo_letters,
                   'letter': target_letter, 'sender': target_madadjoo, 'receiver': target_madadkar})


@madadkar_login_required
def delete_letter_madadkar(request):
    models.madadjoo_madadkar_letter.objects.get(id=request.GET.get('letter', '')).delete()
    all_madadjoo_madadkar_letters = \
        madadjoo_madadkar_letter.objects.filter(madadkar_id=request.user.id)
    all_madadjoo_hamyar_letters = \
        madadjoo_hamyar_letter.objects.filter(madadjoo__corr_madadkar=request.user.id, confirmed=0)
    all_hamyar_madadjoo_letters = \
        hamyar_madadjoo_meeting.objects.filter(madadjoo__corr_madadkar=request.user.id)
    return render(request, 'madadkar/inbox.html',
                  {'madadjoo_madadkar_letters': all_madadjoo_madadkar_letters,
                   'madadjoo_hamyar_letters': all_madadjoo_hamyar_letters,
                   'hamyar_madadjoo_letters': all_hamyar_madadjoo_letters})


@hamyar_login_required
def delete_letter_hamyar(request):
    models.madadjoo_hamyar_letter.objects.get(id=request.GET.get('letter', '')).delete()
    all_letters = madadjoo_hamyar_letter.objects.filter(hamyar_id=request.user.id, confirmed=1)
    return render(request, 'hamyar/inbox.html', {'letters': all_letters})


@madadkar_login_required
def letter_mtoh_content_madadkar(request):
    target_letter = models.madadjoo_hamyar_letter.objects.get(id=request.GET.get('letter', ''))
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_hamyar = models.hamyar.objects.get(active_user_ptr_id=target_letter.hamyar_id)
    all_madadjoo_madadkar_letters = \
        madadjoo_madadkar_letter.objects.filter(madadkar_id=request.user.id)
    all_madadjoo_hamyar_letters = \
        madadjoo_hamyar_letter.objects.filter(madadjoo__corr_madadkar=request.user.id, confirmed=0)
    all_hamyar_madadjoo_letters = \
        hamyar_madadjoo_meeting.objects.filter(madadjoo__corr_madadkar=request.user.id)
    return render(request, 'madadkar/letter_content.html',
                  {'madadjoo_madadkar_letters': all_madadjoo_madadkar_letters,
                   'madadjoo_hamyar_letters': all_madadjoo_hamyar_letters,
                   'hamyar_madadjoo_letters': all_hamyar_madadjoo_letters,
                   'letter': target_letter, 'sender': target_madadjoo, 'receiver': target_hamyar})


@madadkar_login_required
def letter_htom_content_madadkar(request):
    target_letter = models.hamyar_madadjoo_meeting.objects.get(id=request.GET.get('letter', ''))
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_hamyar = models.hamyar.objects.get(active_user_ptr_id=target_letter.hamyar_id)
    all_madadjoo_madadkar_letters = \
        madadjoo_madadkar_letter.objects.filter(madadkar_id=request.user.id)
    all_madadjoo_hamyar_letters = \
        madadjoo_hamyar_letter.objects.filter(madadjoo__corr_madadkar=request.user.id, confirmed=0)
    all_hamyar_madadjoo_letters = \
        hamyar_madadjoo_meeting.objects.filter(madadjoo__corr_madadkar=request.user.id)
    return render(request, 'madadkar/letter_content_removable.html',
                  {'madadjoo_madadkar_letters': all_madadjoo_madadkar_letters,
                   'madadjoo_hamyar_letters': all_madadjoo_hamyar_letters,
                   'hamyar_madadjoo_letters': all_hamyar_madadjoo_letters,
                   'letter': target_letter, 'sender': target_hamyar, 'receiver': target_madadjoo})


@hamyar_login_required
def letter_content_hamyar(request):
    target_letter = models.madadjoo_hamyar_letter.objects.get(id=request.GET.get('letter', ''), confirmed = 0)
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_hamyar = models.hamyar.objects.get(active_user_ptr_id=target_letter.hamyar_id)
    all_letters = madadjoo_hamyar_letter.objects.filter(hamyar_id=request.user.id)

    return render(request, 'hamyar/letter_content.html',
                  {'letters': all_letters, 'letter': target_letter,
                   'sender': target_madadjoo, 'receiver': target_hamyar})


@hamyar_login_required
def inbox_hamyar(request):
    all_letters = madadjoo_hamyar_letter.objects.filter(hamyar_id=request.user.id, confirmed = 0)
    return render(request, 'hamyar/inbox.html', {'letters': all_letters})


@madadkar_login_required
def madadkar_panel(request):
    return render(request, 'madadkar/madadkar_panel.html')


@hamyar_login_required
def hamyar_panel(request):
    return render(request, 'hamyar/hamyar_panel.html')


@hamyar_login_required
def show_hamyar_information(request):
    active_user = models.active_user.objects.get(username=request.user)
    hamyar = models.hamyar.objects.get(active_user_ptr_id=active_user.id)
    user = {'first_name': active_user.first_name,
            'last_name': active_user.last_name,
            'id_number': active_user.id_number,
            'phone_number': active_user.phone_number,
            'email': active_user.email,
            'address': active_user.address,
            }
    madadjoos = madadjoo.objects.filter(sponsership__hamyar_id=active_user.id)
    return render(request, 'hamyar/show_details.html', {'madadjoos': madadjoos})

@hamyar_login_required
@csrf_exempt
def edit_hamyar_information(request):
    if request.method == 'GET':
        return render(request, 'hamyar/edit_details.html')
    else:
        user = hamyar.objects.get(username=request.user)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.id_number = request.POST.get('id_number')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        user.email = request.POST.get('email')
        if request.POST.get('profile_pic') != '':
            user.profile_pic = request.POST.get('profile_pic')
        try:
            user.save()
            return HttpResponseRedirect(reverse("hamyar_panel"))  # this should be hamyar's own page
        except IntegrityError:
            return render(request, 'hamyar/edit_details.html', {'message': 'کد ملی باید یکتا باشد.'})


@hamyar_login_required
def payment_reports(request):
    return render(request, 'hamyar/payment_reports.html')


@hamyar_login_required
def select_madadjoo(request):
    # all_madadjoo = list(madadjoo.objects.values('id', 'username', 'first_name', 'last_name', 'bio'))
    # corr_madadjoos = list(sponsership.objects.filter(hamyar_id=request.user.id).values('madadjoo_id'))
    # corr_madadjoos_id = [list(x.values())[0] for x in corr_madadjoos]
    #
    # not_rel_madadjoos = list()
    #
    # for madadjoo_dict in all_madadjoo:
    #     if madadjoo_dict['id'] not in corr_madadjoos_id:
    #         not_rel_madadjoos.append(madadjoo_dict)

    not_rel_madadjoos = madadjoo.objects.exclude(sponsership__hamyar_id=request.user.id)

    return render(request, 'hamyar/select_madadjoo.html', {'madadjoos': not_rel_madadjoos})


@hamyar_login_required
def show_madadjoo_report(request):
    return render(request, 'hamyar/madadjoo_report.html')


@madadjoo_login_required
def madadjoo_panel(request):
    return render(request, 'madadjoo/madadjoo_panel.html')


@madadjoo_login_required
def show_hamyar(request):
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=request.user.id)
    return render(request, 'madadjoo/show_hamyar.html', {'hamyars': hamyars})


@madadjoo_login_required
def show_a_madadkar_madadjoo(request):
    madadkar_id = models.madadjoo.objects.get(username=request.user).corr_madadkar_id
    if madadkar_id == None:
        return render(request, 'madadjoo/show_a_madadkar.html',
                      {'first_name': 'مدیر سامانه', 'last_name': 'مدیر سامانه'})
    target_madadkar = models.madadkar.objects.get(active_user_ptr_id=madadkar_id)
    try:
        target_madadkar.profile_pic
        return render(request, 'madadjoo/show_a_madadkar.html',
                      {'first_name': target_madadkar.first_name, 'last_name': target_madadkar.last_name,
                       'username': target_madadkar.username, 'profile_pic': target_madadkar.profile_pic})
    except Exception:
        return render(request, 'madadjoo/show_a_madadkar.html',
                      {'first_name': target_madadkar.first_name, 'last_name': target_madadkar.last_name,
                       'username': target_madadkar.username, 'profile_pic': None})


@madadjoo_login_required
def show_a_hamyar_madadjoo(request):
    target_hamyar = hamyar.objects.get(username=request.GET.get('username', ''))
    return render(request, 'madadjoo/show_a_hamyar.html', {'hamyar': target_hamyar})


@madadjoo_login_required
def payment_reports_madadjoo(request):
    return render(request, 'madadjoo/payment_reports.html')


@madadjoo_login_required
def send_letter_hamyar_madadjoo(request):
    target_hamyar = hamyar.objects.get(username=request.GET.get('username', ''))
    user = madadjoo.objects.get(username=request.user)
    if request.method == "GET":
        return render(request, 'madadjoo/send_gratitude_letter.html', {'user': user, 'receiver': target_hamyar})
    else:
        title = request.POST.get('title')
        text = request.POST.get('text')
        letter = madadjoo_hamyar_letter(madadjoo=user, hamyar=target_hamyar, text=text, title=title,
                                        confirmed=False)
        letter.save()
        return HttpResponseRedirect(reverse("madadjoo_panel"))


@madadjoo_login_required
def send_request_madadkar(request):
    target_madadkar = madadkar.objects.get(username=request.GET.get('username', ''))
    user = madadjoo.objects.get(username=request.user)
    if request.method == "GET":
        return render(request, 'madadjoo/send_request_madadkar.html', {'user': user, 'receiver': target_madadkar})
    else:
        title = request.POST.get('title')
        text = request.POST.get('text')
        letter = madadjoo_madadkar_letter(madadjoo=user, madadkar=target_madadkar, text=text, title=title,
                                          thank=False)
        letter.save()
        return HttpResponseRedirect(reverse("madadjoo_panel"))


@madadjoo_login_required
def send_gratitude_letter(request):
    target_madadkar = madadkar.objects.get(username=request.GET.get('username', ''))
    user = madadjoo.objects.get(username=request.user)
    if request.method == "GET":
        return render(request, 'madadjoo/send_gratitude_letter.html', {'user': user, 'receiver': target_madadkar})
    else:
        title = request.POST.get('title')
        text = request.POST.get('text')
        letter = madadjoo_madadkar_letter(madadjoo=user, madadkar=target_madadkar, text=text, title=title,
                                          thank=True)
        letter.save()
        return HttpResponseRedirect(reverse("madadjoo_panel"))


@madadjoo_login_required
def show_madadjoo_information(request):
    active_user = models.active_user.objects.get(username=request.user)
    madadjoo = models.madadjoo.objects.get(active_user_ptr_id=active_user.id)
    needs = models.requirements.objects.get(madadjoo_id=active_user.id)
    user = {'first_name': active_user.first_name,
            'last_name': active_user.last_name,
            'id_number': active_user.id_number,
            'phone_number': active_user.phone_number,
            'email': active_user.email,
            'address': active_user.address,
            'invest': madadjoo.invest_percentage,
            'successes': madadjoo.successes,
            'bio': madadjoo.bio,
            'edu_status': madadjoo.edu_status,
            'profile_pic': madadjoo.profile_pic,
            'need': {'description': needs.description, 'type': needs.type, 'urgent': needs.urgent, 'cash': needs.cash}
            }
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=active_user.id)
    return render(request, 'madadjoo/show_madadjoo_information.html', {'user': user, 'hamyars': hamyars})


@admin_login_required
def admin_panel(request):
    print(request.session['type'])
    return render(request, 'admin/admin_panel.html')


@admin_login_required
def show_madadjoo_admin(request):
    return render(request, 'admin/show_madadjoo.html')


@login_required(login_url='/login')
def show_a_madadjoo_admin(request):
    return render(request, 'admin/show_a_madadjoo.html')


@admin_login_required
def edit_a_madadjoo_admin(request):
    return render(request, 'admin/edit_a_madadjoo.html')


@admin_login_required
def inbox_admin(request):
    return render(request, 'admin/inbox.html')


@admin_login_required
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


@madadkar_login_required
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
        profile_pic = request.FILES.get('profile_pic')
        print(profile_pic)
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
                                       invest_percentage=invest_percentage, corr_madadkar=corr_madadkar,
                                       confirmed=False,
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


@admin_login_required
def show_madadkar_admin(request):
    return render(request, 'admin/show_madadkar.html')


@admin_login_required
def show_a_madadkar_admin(request):
    return render(request, 'admin/show_a_madadkar.html')


@admin_login_required
def edit_a_madadkar_admin(request):
    return render(request, 'admin/edit_a_madadkar.html')


@admin_login_required
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


@admin_login_required
def show_hamyar_admin(request):
    return render(request, 'admin/show_hamyar.html')


@admin_login_required
def show_a_hamyar_admin(request):
    return render(request, 'admin/show_a_hamyar.html')


@admin_login_required
def edit_a_hamyar_admin(request):
    return render(request, 'admin/edit_a_hamyar.html')


@admin_login_required
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


@admin_login_required
def payment_reports_admin(request):
    return render(request, 'admin/payment_reports.html')


@admin_login_required
def activity_report(request):
    return render(request, 'admin/activity_reports.html')


@admin_login_required
def madadjoo_paid_report(request):
    return render(request, 'admin/madadjoo_paid_report.html')
