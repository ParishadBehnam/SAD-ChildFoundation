# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from actstream import action
from actstream.models import target_stream, actor_stream
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from active_user import forms
from active_user import models
from active_user.decorators import admin_login_required
from active_user.decorators import madadkar_login_required
from active_user.decorators import hamyar_login_required
from active_user.decorators import madadjoo_login_required
from active_user.decorators import madadkar_login_required
from active_user.models import madadjoo, hamyar, madadkar, sponsership, \
    madadjoo_madadkar_letter, madadjoo_hamyar_letter, hamyar_madadjoo_meeting, \
    hamyar_system_payment, hamyar_madadjoo_payment, requirements, hamyar_madadjoo_non_cash, add_madadjoo_admin_letter, \
    madadkar_remove_madadjoo, urgent_need_admin_letter, admin_user, warning_admin_letter, active_user, \
    substitute_a_madadjoo, request_for_change_madadkar
from system import models as system_models
from system.models import information


@madadkar_login_required
def home_madadkar(request):
    system = information.objects.first()
    return render(request, 'madadkar/home_madadkar.html', {'system': system})


@hamyar_login_required
def home_hamyar(request):
    system = information.objects.first()
    return render(request, 'hamyar/home_hamyar.html', {'system': system})


@madadjoo_login_required
def home_madadjoo(request):
    system = information.objects.first()
    return render(request, 'madadjoo/home_madadjoo.html', {'system': system})


@admin_login_required
def home_admin(request):
    system = information.objects.first()
    return render(request, 'admin/home_admin.html', {'system': system})


@madadkar_login_required
def show_madadjoo(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_madadjoo = madadjoo.objects.filter(corr_madadkar=request.user.id).exclude(
        active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'madadkar/show_madadjoo.html', {'madadjoos': all_madadjoo})


@hamyar_login_required
def show_madadjoo_hamyar(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_madadjoo = madadjoo.objects.filter(sponsership__hamyar_id=request.user.id, confirmed=True).exclude(
        active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'hamyar/show_madadjoo.html', {'madadjoos': all_madadjoo})


@madadkar_login_required
def show_madadjoo_madadkar(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_madadjoo = madadjoo.objects.filter(corr_madadkar=None, confirmed=True).exclude(
        active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'madadkar/show_not_mine_madadjoo.html', {'madadjoos': all_madadjoo})


@madadkar_login_required
def edit_madadjoo(request):
    if request.method == "GET":
        target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
        needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
        return render(request, 'madadkar/edit_madadjoo_full.html',
                      {'user': target_madadjoo, 'needs': needs})
    else:
        warning_message = False
        user_madadkar = madadkar.objects.get(username=request.user.username)
        user = madadjoo.objects.get(username=request.GET.get('username', ''))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.id_number = request.POST.get('id_number')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        user.email = request.POST.get('email')
        user.bio = request.POST.get('bio')
        user.edu_status = request.POST.get('edu_status')
        user.successes = request.POST.get('successes')
        user.invest_percentage = request.POST.get('invest_percentage')
        if request.POST.get('profile_pic') != '':
            user.profile_pic = request.FILES.get('profile_pic')

        all_reqs = requirements.objects.filter(madadjoo_id=user.id)
        for req in all_reqs:
            prev_req = requirements.objects.get(id=req.id)
            prev_req.description = request.POST.get('description_base' + str(req.id))
            prev_req.cash = True if request.POST.get('cash_base' + str(req.id)) == "cash" else False
            urgent = True if request.POST.get('urgent_base' + str(req.id)) == "urgent" else False
            if not prev_req.urgent and urgent:
                new_letter = urgent_need_admin_letter(madadjoo=user, madadkar=user_madadkar, need=prev_req)
                new_letter.save()
                warning_message = True
                urgent = False
            prev_req.urgent = urgent
            prev_req.type = request.POST.get('type_base' + str(req.id))
            prev_req.confirmed = False if req.urgent else True
            prev_req.save()
            index = 0

        for desc in request.POST.getlist('description'):
            if desc != "":
                description = desc
                type = request.POST.get('type' + str(index))
                cash = True if request.POST.get('cash' + str(index)) == "cash" else False
                urgent = True if request.POST.get('urgent' + str(index)) == "urgent" else False
                confirmed = False if urgent else True

                new_req = requirements(description=description, type=type, cash=cash, urgent=urgent,
                                       confirmed=confirmed, madadjoo_id=user.id)
                new_req.save()
                if urgent:
                    new_letter = urgent_need_admin_letter(madadjoo=user, madadkar=user_madadkar, need=new_req)
                    new_letter.save()
                    warning_message = True
                    new_req.urgent = False
                    new_req.save()

            index += 1

        target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
        needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
        try:
            action.send(request.user, verb='ویرایش مشخصات مددجو', target=target_madadjoo)
            user.save()
            s = 'اطلاعات مددجو با موفقیت ویرایش شد.'
            if warning_message:
                w = 'نیاز‌/نیاز‌های فوری ثبت شده بعد از تایید مدیر نهایی خواهند شد'
                return render(request, 'madadkar/edit_madadjoo_full.html',
                              {'user': user, 'needs': needs, 'success_message': s, 'warning_message': w})
            return render(request, 'madadkar/edit_madadjoo_full.html',
                          {'user': user, 'needs': needs, 'success_message': s})
        except IntegrityError:
            return render(request, 'madadkar/edit_madadjoo_full.html',
                          {'user': target_madadjoo, 'needs': needs, 'error_message': 'کد ملی باید یکتا باشد.'})


@madadkar_login_required
def add_madadjoo(request):
    return render(request, 'madadkar/add_madadjoo.html')


@madadkar_login_required
def show_a_madadjoo(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)
    return render(request, 'madadkar/show_a_madadjoo.html',
                  {'user': target_madadjoo, 'needs': needs, 'hamyars': hamyars})


@madadkar_login_required
def show_a_not_mine_madadjoo(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)
    return render(request, 'madadkar/show_a_not_mine_madadjoo.html',
                  {'user': target_madadjoo, 'needs': needs, 'hamyars': hamyars})


@hamyar_login_required
def support_a_madadjoo(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    target_hamyar = hamyar.objects.get(id=request.user.id)
    new_sponsership = sponsership(hamyar_id=target_hamyar.id, madadjoo_id=target_madadjoo.id)
    new_sponsership.save()
    deleted_mdadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_madadjoo = madadjoo.objects.filter(confirmed=True) \
        .exclude(sponsership__hamyar_id=request.user.id).exclude(active_user_ptr_id__in=deleted_mdadjoos)

    action.send(request.user, verb='حمایت از مددجو', target=target_madadjoo)
    return render(request, 'hamyar/select_madadjoo.html',
                  {'madadjoos': list(all_madadjoo), 'success_message': 'مددجوی مورد نظر تحت حمایت شما قرار گرفت'})



@madadkar_login_required
def support_a_madadjoo_madadkar(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    target_madadkar = madadkar.objects.get(id=request.user.id)
    target_madadjoo.corr_madadkar = target_madadkar
    target_madadjoo.save()
    deleted_mdadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_madadjoo = madadjoo.objects.filter(confirmed=True, corr_madadkar=None).\
        exclude(active_user_ptr_id__in=deleted_mdadjoos)

    action.send(request.user, verb='حمایت از مددجوی بدون حامی', target=target_madadjoo)
    return render(request, 'madadkar/show_not_mine_madadjoo.html',
                  {'madadjoos': list(all_madadjoo), 'success_message': 'مددجوی مورد نظر تحت حمایت شما قرار گرفت'})




@hamyar_login_required
def substitute_madadjoo(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('target', ''))
    target_hamyar = request.user
    removed_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    remove = madadkar_remove_madadjoo.objects.get(madadjoo=removed_madadjoo, hamyar_id=target_hamyar.id)

    print(target_madadjoo, target_hamyar, removed_madadjoo, remove.id)
    new_sponsership = sponsership(hamyar_id=target_hamyar.id, madadjoo_id=target_madadjoo.id)
    new_sponsership.save()

    new_substitution = substitute_a_madadjoo(remove_id=remove.id, substituted_madadjoo_id=target_madadjoo.id)
    new_substitution.save()

    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_letters = madadjoo_hamyar_letter.objects.filter(hamyar_id=request.user.id, confirmed=1).exclude(
        madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    delete_letters = madadkar_remove_madadjoo.objects.filter(hamyar_id=request.user.id)
    action.send(request.user, verb='حمایت از مددجو', target=target_madadjoo)
    return render(request, 'hamyar/inbox.html', {'letters': all_letters, 'delete_letters': delete_letters,
                                                 'success_message': 'مددجوی جدید با موفقیت تحت حمایت شما قرار گرفت.'})


@hamyar_login_required
def show_a_madadjoo_hamyar(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)
    true = sponsership.objects.filter(hamyar_id=request.user.id, madadjoo_id=target_madadjoo.active_user_ptr_id)
    if request.method == 'GET':
        if true:
            return render(request, 'hamyar/show_a_madadjoo.html',
                          {'user': target_madadjoo, 'needs': needs, 'hamyars': hamyars})
        return render(request, 'hamyar/show_a_stranger.html',
                      {'user': target_madadjoo, 'needs': needs, 'hamyars': hamyars})

    else:
        target_hamyar = hamyar.objects.get(id=request.user.id)
        if 'help' in request.POST:
            text = request.POST.get('help')
            if text != '':
                help = hamyar_madadjoo_non_cash(madadjoo=target_madadjoo, hamyar=target_hamyar, text=text)
                help.save()
                return render(request, 'hamyar/show_a_madadjoo.html', {'user': target_madadjoo, 'needs': needs,
                                                                       'hamyars': hamyars,
                                                                       'success_message': 'کمک شما با موفقیت در سامانه ثبت شد.'})
            return render(request, 'hamyar/show_a_madadjoo.html', {'user': target_madadjoo, 'needs': needs,
                                                                   'hamyars': hamyars,
                                                                   'error_message': 'لطفا توضیح از کمک خود را وارد کنید.'})
        else:
            need_id = request.POST.get('need')
            if need_id:
                need = requirements.objects.get(id=need_id)
                amount = request.POST.get('amount')
                if amount != '':
                    if need.type:
                        type = need.type
                    else:
                        type = 'inst'
                    payment = hamyar_madadjoo_payment(madadjoo=target_madadjoo, hamyar=target_hamyar,
                                                      amount=amount, type=type, need=need)
                    payment.save()

                    type = 'ماهانه' if type == 'mo' else 'سالانه' if type == 'ann' else 'موردی'
                    message = target_madadjoo.first_name + ' ' + target_madadjoo.last_name + 'عزیز، \n پرداخت از سوی ' + \
                              target_hamyar.first_name + ' ' + target_hamyar.last_name + ' به مبلغ ' + \
                              str(payment.amount) + ' تومان به صورت ' + type + ' در سامانه ثبت گردید.' + \
                              '\n\nبنیاد حمایت از کودکان'

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login('childf2018', 'childF20182018')
                    msg = MIMEMultipart()
                    msg['From'] = 'childf2018@gmail.com'
                    msg['To'] = target_madadjoo.email
                    msg['Subject'] = 'ثبت پرداخت'
                    msg.attach(MIMEText(message, 'plain'))
                    server.send_message(msg)
                    server.quit()

                    action.send(request.user, verb='پرداخت به مددجو', target=target_madadjoo)

                    return render(request, 'hamyar/show_a_madadjoo.html', {'user': target_madadjoo, 'needs': needs,
                                                                           'hamyars': hamyars,
                                                                           'success_message': 'پرداخت شما با موفقیت انجام شد.'})
                return render(request, 'hamyar/show_a_madadjoo.html', {'user': target_madadjoo, 'needs': needs,
                                                                       'hamyars': hamyars,
                                                                       'error_message': 'لطفا مبلغ مورد نظر خود را وارد کنید.'})
            return render(request, 'hamyar/show_a_madadjoo.html', {'user': target_madadjoo, 'needs': needs,
                                                                   'hamyars': hamyars,
                                                                   'error_message': 'لطفا نیاز مورد نظر خود را علامت بزنید.'})


@madadkar_login_required
def show_a_hamyar(request):
    target_hamyar = hamyar.objects.get(username=request.GET.get('username', ''))
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    madadjoos = madadjoo.objects.filter(corr_madadkar_id=request.user.id, sponsership__hamyar_id=target_hamyar.id,
                                        confirmed=True).exclude(active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'madadkar/show_a_hamyar.html', {'hamyar': target_hamyar, 'madadjoos': madadjoos})


@madadkar_login_required
def send_letter(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username'))
    target_madadkar = madadkar.objects.get(id=request.user.id)
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)
    if request.method == 'GET':
        return render(request, 'madadkar/send_letter.html', {'hamyars': hamyars})
    else:
        target_hamyars = request.POST.getlist('receiver')
        text = request.POST.get('text')
        if text != '':
            for h_id in target_hamyars:
                h = hamyar.objects.get(id=h_id)
                removed = madadkar_remove_madadjoo(text=text, madadjoo=target_madadjoo,
                                                   hamyar=h, madadkar=target_madadkar)
                action.send(request.user, verb="مددجو را از سامانه حذف کرد", target=target_madadjoo)

                removed.save()
            return HttpResponseRedirect(reverse('madadkar_panel') + '?success=3')
        else:
            return render(request, 'madadkar/send_letter.html', {'hamyars': hamyars,
                                                                 'error_message': 'لطفا متن اطلاع‌رسانی را پر نمایید.'})


@admin_login_required
def send_delete_letter(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username'))
    target_admin = admin_user.objects.get(id=request.user.id)
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)
    if request.method == 'GET':
        return render(request, 'admin/send_delete_letter.html', {'hamyars': hamyars})
    else:
        target_hamyars = request.POST.getlist('receiver')
        text = request.POST.get('text')
        if text != '':
            for h_id in target_hamyars:
                h = hamyar.objects.get(id=h_id)
                removed = madadkar_remove_madadjoo(text=text, madadjoo=target_madadjoo,
                                                   hamyar=h, madadkar=None)
                removed.save()
            return HttpResponseRedirect(reverse('admin_panel') + '?success=3')
        else:
            return render(request, 'madadkar/send_letter.html', {'hamyars': hamyars,
                                                                 'error_message': 'لطفا متن اطلاع‌رسانی را پر نمایید.'})


@hamyar_login_required
def send_letter_hamyar(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username'))
    target_hamyar = hamyar.objects.get(id=request.user.id)
    meeting = hamyar_madadjoo_meeting(hamyar=target_hamyar, madadjoo=target_madadjoo)
    meeting.save()
    return render(request, 'hamyar/show_a_madadjoo.html', {'user': target_madadjoo,
                                                           'success_message': 'درخواست ملاقات شما با موفقیت در سامانه ثبت گردید'})


@hamyar_login_required
def stop_support_hamyar(request):
    amount = models.hamyar_madadjoo_payment.objects.filter(hamyar_id=request.user.id, madadjoo__active_user_ptr_id=request.GET.get('madadjoo', ''))
    sum = 0
    for a in amount:
        sum += a.amount
    amount.delete()
    our_system = list(system_models.information.objects.all())
    if sum>0 :
        payment = hamyar_system_payment(amount=sum, hamyar_id=request.user.id, system_id=our_system[0].history)
    payment.save()
    models.sponsership.objects.get(hamyar_id=request.user.id, madadjoo__active_user_ptr_id=request.GET.get('madadjoo', '')).delete()
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    d = show_madadjoo(request)
    d['success_message'] = 'عدم حمایت از مددجو با موفقیت ثبت گردید.'
    all_madadjoo = madadjoo.objects.filter(sponsership__hamyar_id=request.user.id, confirmed=True).exclude(
        active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'hamyar/show_madadjoo.html', {'madadjoos': all_madadjoo})


def show_letters_madadkar(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_madadjoo_madadkar_letters = \
        madadjoo_madadkar_letter.objects.filter(madadkar_id=request.user.id).exclude(
            madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    all_madadjoo_hamyar_letters = \
        madadjoo_hamyar_letter.objects.filter(madadjoo__corr_madadkar=request.user.id, confirmed=False).exclude(
            madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    all_hamyar_madadjoo_letters = \
        hamyar_madadjoo_meeting.objects.filter(madadjoo__corr_madadkar=request.user.id, confirmed=False).exclude(
            madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    all_warnings = warning_admin_letter.objects.filter(madadkar=request.user.id)
    return {'madadjoo_madadkar_letters': all_madadjoo_madadkar_letters,
            'madadjoo_hamyar_letters': all_madadjoo_hamyar_letters,
            'hamyar_madadjoo_letters': all_hamyar_madadjoo_letters,
            'warnings': all_warnings}


@madadkar_login_required
def inbox_madadkar(request):
    d = show_letters_madadkar(request)
    return render(request, 'madadkar/inbox.html', d)


@madadkar_login_required
def letter_madadjoo_content_madadkar(request):
    target_letter = models.madadjoo_madadkar_letter.objects.get(id=request.GET.get('letter', ''))
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_madadkar = models.madadkar.objects.get(active_user_ptr_id=target_letter.madadkar_id)
    d = show_letters_madadkar(request)
    d['letter'] = target_letter
    d['sender'] = target_madadjoo
    d['receiver'] = target_madadkar
    return render(request, 'madadkar/letter_content_removable.html', d)


@madadkar_login_required
def delete_letter_madadkar(request):
    models.madadjoo_madadkar_letter.objects.get(id=request.GET.get('letter', '')).delete()
    d = show_letters_madadkar(request)
    d['success_message'] = 'نامه با موفقیت حذف گردید.'
    return render(request, 'madadkar/inbox.html', d)


@admin_login_required
def delete_letter_admin(request):
    models.madadjoo_madadkar_letter.objects.get(id=request.GET.get('letter', '')).delete()
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    add_madadjoo_letters = add_madadjoo_admin_letter.objects.all()
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    return render(request, 'admin/inbox.html',
                  {'add_madadjoo_letters': add_madadjoo_letters, 'madadjoo_letters': madadjoo_letters,
                   'urgent_need_letters': urgent_need_letters, 'change_madadkar_letters': change_madadkar_letters,
                   'success_message': 'نامه با موفقیت حذف گردید.'})


@hamyar_login_required
def delete_letter_hamyar(request):
    models.madadjoo_hamyar_letter.objects.get(id=request.GET.get('letter', '')).delete()
    all_letters = madadjoo_hamyar_letter.objects.filter(hamyar_id=request.user.id, confirmed=1)
    return render(request, 'hamyar/inbox.html',
                  {'letters': all_letters, 'success_message': 'نامه با موفقیت حذف گردید.'})


@madadkar_login_required
def warning_content_madadkar(request):
    target_letter = warning_admin_letter.objects.get(id=request.GET.get('letter', ''))
    d = show_letters_madadkar(request)
    d['letter'] = target_letter
    d['sender'] = target_letter.admin_user
    d['receiver'] = target_letter.madadkar
    return render(request, 'madadkar/letter_warning_content.html', d)


@madadkar_login_required
def letter_mtoh_content_madadkar(request):
    target_letter = models.madadjoo_hamyar_letter.objects.get(id=request.GET.get('letter', ''))
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_hamyar = models.hamyar.objects.get(active_user_ptr_id=target_letter.hamyar_id)
    d = show_letters_madadkar(request)
    d['letter'] = target_letter
    d['sender'] = target_madadjoo
    d['receiver'] = target_hamyar
    return render(request, 'madadkar/letter_content.html', d)


@madadkar_login_required
def letter_htom_content_madadkar(request):
    target_letter = models.hamyar_madadjoo_meeting.objects.get(id=request.GET.get('letter', ''), confirmed=False)
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_hamyar = models.hamyar.objects.get(active_user_ptr_id=target_letter.hamyar_id)
    d = show_letters_madadkar(request)
    d['letter'] = target_letter
    d['sender'] = target_hamyar
    d['receiver'] = target_madadjoo
    return render(request, 'madadkar/letter_content_htom.html', d)


@madadkar_login_required
def confirm_madadjoo_hamyar_letter(request):
    letter = madadjoo_hamyar_letter.objects.get(id=request.GET.get('letter'))
    letter.confirmed = True
    letter.save()
    d = show_letters_madadkar(request)
    d['success_message'] = 'نامه با موفقیت تایید گردید.'
    return render(request, 'madadkar/inbox.html', d)


@madadkar_login_required
def confirm_hamyar_madadjoo_letter(request):
    letter = hamyar_madadjoo_meeting.objects.get(id=request.GET.get('letter'))
    letter.confirmed = True
    letter.save()
    d = show_letters_madadkar(request)
    d['success_message'] = 'درخواست ملاقات با موفقیت تایید گردید.'
    action(request.user, verb="درخواست ملاقات با مددجو را تایید کرد", action_object=letter.hamyar,
           target=letter.madadjoo)
    return render(request, 'madadkar/inbox.html', d)


@hamyar_login_required
def select_to_substitute_a_madadjoo_hamyar(request):
    removed_madadjoo = madadjoo.objects.get(username=request.GET.get('username'))
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    not_rel_madadjoos = madadjoo.objects.exclude(sponsership__hamyar_id=request.user.id)
    not_rel_madadjoos = not_rel_madadjoos.exclude(confirmed=False).exclude(active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'hamyar/substitute_a_madadjoo.html', {'removed': removed_madadjoo,
                                                                 'madadjoos': not_rel_madadjoos})


@hamyar_login_required
def letter_content_hamyar(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    target_letter = models.madadjoo_hamyar_letter.objects.get(id=request.GET.get('letter', ''), confirmed=1)
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_hamyar = models.hamyar.objects.get(active_user_ptr_id=target_letter.hamyar_id)
    all_letters = madadjoo_hamyar_letter.objects.filter(hamyar_id=request.user.id).exclude(
        madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    delete_letters = madadkar_remove_madadjoo.objects.filter(hamyar_id=request.user.id)
    return render(request, 'hamyar/letter_content.html',
                  {'letters': all_letters, 'delete_letters': delete_letters, 'letter': target_letter,
                   'sender': target_madadjoo, 'receiver': target_hamyar})


@madadjoo_login_required
def letter_content_madadjoo(request):
    target_letter = hamyar_madadjoo_meeting.objects.get(id=request.GET.get('letter', ''), confirmed=True)
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_hamyar = models.hamyar.objects.get(active_user_ptr_id=target_letter.hamyar_id)
    all_letters = hamyar_madadjoo_meeting.objects.filter(madadjoo_id=request.user.id, confirmed=True)
    return render(request, 'madadjoo/letter_content.html',
                  {'letters': all_letters, 'letter': target_letter,
                   'sender': target_hamyar, 'receiver': target_madadjoo})


@hamyar_login_required
def delete_madadjoo_letter_content_hamyar(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    target_letter = madadkar_remove_madadjoo.objects.get(id=request.GET.get('letter', ''))
    try:
        substitute_a_madadjoo.objects.get(remove=target_letter)
        is_subs = True
    except:
        is_subs = False
    target_madadjoo = models.madadjoo.objects.get(active_user_ptr_id=target_letter.madadjoo_id)
    target_hamyar = models.hamyar.objects.get(active_user_ptr_id=target_letter.hamyar_id)
    if target_letter.madadkar_id:
        target_madadkar = models.madadkar.objects.get(active_user_ptr_id=target_letter.madadkar_id)
    else:
        target_madadkar = None
    all_letters = madadjoo_hamyar_letter.objects.filter(hamyar_id=request.user.id).exclude(
        madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    delete_letters = madadkar_remove_madadjoo.objects.filter(hamyar_id=request.user.id)
    return render(request, 'hamyar/letter_content.html',
                  {'letters': all_letters, 'delete_letters': delete_letters, 'letter': target_letter,
                   'is_substituted': is_subs, 'sender': target_madadkar, 'receiver': target_hamyar,
                   'madadjoo': target_madadjoo})


@hamyar_login_required
def inbox_hamyar(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_letters = madadjoo_hamyar_letter.objects.filter(hamyar_id=request.user.id, confirmed=1).exclude(
        madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    delete_letters = madadkar_remove_madadjoo.objects.filter(hamyar_id=request.user.id)
    return render(request, 'hamyar/inbox.html', {'letters': all_letters, 'delete_letters': delete_letters})


@madadjoo_login_required
def inbox_madadjoo(request):
    all_letters = hamyar_madadjoo_meeting.objects.filter(madadjoo_id=request.user.id, confirmed=True)
    return render(request, 'madadjoo/inbox.html', {'letters': all_letters})


@madadkar_login_required
def madadkar_panel(request):
    if request.GET.get('success') == '1':
        print(request.user)
        return render(request, 'madadkar/madadkar_panel.html', {'success_message': request.user.first_name + ' ' +
                                                                                   request.user.last_name + ' عزیز، شما با موفقیت وارد حساب کاربری خود شدید :)'})
    elif request.GET.get('success') == '3':
        return render(request, 'madadkar/madadkar_panel.html',
                      {'success_message': 'پیغام شما با موفقیت به همیاران ارسال شد.'})
    return render(request, 'madadkar/madadkar_panel.html')


@hamyar_login_required
def hamyar_panel(request):
    if request.method == 'GET':
        if request.GET.get('success') == '1':
            return render(request, 'hamyar/hamyar_panel.html', {'success_message': request.user.first_name + ' ' +
                                                                                   request.user.last_name + ' عزیز، شما با موفقیت وارد حساب کاربری خود شدید :)'})
        return render(request, 'hamyar/hamyar_panel.html')
    else:
        amount = request.POST.get('amount')
        our_system = list(system_models.information.objects.all())
        payment = hamyar_system_payment(amount=amount, hamyar_id=request.user.id, system_id=our_system[0].history)
        payment.save()
        return render(request, 'hamyar/hamyar_panel.html', {'success_message': 'پرداخت شما با موفقیت انجام شد.'})


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
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    madadjoos = madadjoo.objects.filter(sponsership__hamyar_id=active_user.id, confirmed=True).exclude(
        active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'hamyar/show_details.html', {'madadjoos': madadjoos})


@hamyar_login_required
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
        # print(request.FILES)
        # print(request.FILES.get('profile_pic'))
        # print(request.POST.get('profile_pic'))
        if request.POST.get('profile_pic') != '':
            user.profile_pic = request.FILES.get('profile_pic')
        try:
            user.save()
            return render(request, 'hamyar/edit_details.html', {'user': user,
                                                                'success_message': 'اطلاعات شما با موفقیت ویرایش شد.'})  # this should be hamyar's own page
        except IntegrityError:
            return render(request, 'hamyar/edit_details.html', {'error_message': 'کد ملی باید یکتا باشد.'})


@hamyar_login_required
def payment_reports(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    cash = hamyar_madadjoo_payment.objects.filter(hamyar_id=request.user.id).exclude(
        madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    non_cash = hamyar_madadjoo_non_cash.objects.filter(hamyar_id=request.user.id).exclude(
        madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    system = hamyar_system_payment.objects.filter(hamyar_id=request.user.id)

    cash_for_deleteds = hamyar_madadjoo_payment.objects.filter(hamyar_id=request.user.id).filter(
        madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    non_cash_for_deleteds = hamyar_madadjoo_non_cash.objects.filter(hamyar_id=request.user.id).filter(
        madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'hamyar/payment_reports.html', {'cash': cash, 'non_cash': non_cash,
                                                           'system': system,
                                                           'cash_for_deleteds': cash_for_deleteds,
                                                           'non_cash_for_deleteds': non_cash_for_deleteds})


@hamyar_login_required
def select_madadjoo(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    not_rel_madadjoos = madadjoo.objects.exclude(sponsership__hamyar_id=request.user.id)
    not_rel_madadjoos = not_rel_madadjoos.exclude(confirmed=False).exclude(active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'hamyar/select_madadjoo.html', {'madadjoos': not_rel_madadjoos})


@hamyar_login_required
def show_madadjoo_report(request):
    stream = []
    for sponser in sponsership.objects.filter(hamyar_id=request.user.id):
        target_madadjoo = sponser.madadjoo
        stream.append((target_madadjoo, target_stream(target_madadjoo)))

    return render(request, 'hamyar/madadjoo_report.html', {'stream': stream})


@madadjoo_login_required
def madadjoo_panel(request):
    if request.GET.get('success') == '1':
        return render(request, 'madadjoo/madadjoo_panel.html', {'success_message': request.user.first_name + ' ' +
                                                                                   request.user.last_name + ' عزیز، شما با موفقیت وارد حساب کاربری خود شدید :)'})

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
                      {'first_name': 'ندارد', 'last_name': 'ندارد', 'has_madadkar': False})
    target_madadkar = models.madadkar.objects.get(active_user_ptr_id=madadkar_id)
    try:
        target_madadkar.profile_pic
        return render(request, 'madadjoo/show_a_madadkar.html',
                      {'first_name': target_madadkar.first_name, 'last_name': target_madadkar.last_name,
                       'username': target_madadkar.username, 'profile_pic': target_madadkar.profile_pic, 'has_madadkar': True})
    except Exception:
        return render(request, 'madadjoo/show_a_madadkar.html',
                      {'first_name': target_madadkar.first_name, 'last_name': target_madadkar.last_name,
                       'username': target_madadkar.username, 'profile_pic': None, 'has_madadkar': True})


@madadjoo_login_required
def show_a_hamyar_madadjoo(request):
    target_hamyar = hamyar.objects.get(username=request.GET.get('username', ''))
    return render(request, 'madadjoo/show_a_hamyar.html', {'hamyar': target_hamyar})


@madadjoo_login_required
def payment_reports_madadjoo(request):
    cash = hamyar_madadjoo_payment.objects.filter(madadjoo_id=request.user.id)
    non_cash = hamyar_madadjoo_non_cash.objects.filter(madadjoo_id=request.user.id)
    return render(request, 'madadjoo/payment_reports.html', {'cash': cash,
                                                             'non_cash': non_cash})


@madadjoo_login_required
def send_letter_hamyar_madadjoo(request):
    target_hamyar = hamyar.objects.get(username=request.GET.get('username', ''))
    user = madadjoo.objects.get(username=request.user)
    if request.method == "GET":
        return render(request, 'madadjoo/send_letter_hamyar.html', {'user': user, 'hamyar': target_hamyar})
    else:
        title = request.POST.get('title')
        text = request.POST.get('text')
        letter = madadjoo_hamyar_letter(madadjoo=user, hamyar=target_hamyar, text=text, title=title,
                                        confirmed=False)
        letter.save()
        # return HttpResponseRedirect(reverse("madadjoo_panel"))
        return render(request, 'madadjoo/send_letter_hamyar.html', {'user': user, 'hamyar': target_hamyar,
                                                                    'success_message': 'نامه‌ی شما برای تایید به مددکار ارسال شد.'})


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
        # return HttpResponseRedirect(reverse("madadjoo_panel"))
        return render(request, 'madadjoo/send_request_madadkar.html', {'user': user, 'receiver': target_madadkar,
                                                                       'success_message': 'درخواست شما برای مددکار ارسال شد.'})


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
        # return HttpResponseRedirect(reverse("madadjoo_panel"))
        return render(request, 'madadjoo/send_gratitude_letter.html', {'user': user, 'receiver': target_madadkar,
                                                                       'success_message': 'نامه‌ی تشکر شما برای مددکار ارسال شد.'})


@madadjoo_login_required
def request_change_madadkar(request):
    target_madadkar = madadkar.objects.get(username=request.GET.get('username', ''))
    user = madadjoo.objects.get(username=request.user)
    req = request_for_change_madadkar(madadjoo=user)
    req.save()
    return render(request, 'madadjoo/show_a_madadkar.html',
                  {'first_name': target_madadkar.first_name, 'last_name': target_madadkar.last_name,
                   'username': target_madadkar.username, 'profile_pic': target_madadkar.profile_pic,
                   'success_message': 'درخواست شما با موفقیت برای مدیر سامانه ارسال گردید.'})


@madadjoo_login_required
def show_madadjoo_information(request):
    active_user = models.active_user.objects.get(username=request.user)
    madadjoo = models.madadjoo.objects.get(active_user_ptr_id=active_user.id)
    needs = models.requirements.objects.filter(madadjoo_id=active_user.id)
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
            'profile_pic': madadjoo.profile_pic}
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=active_user.id)
    return render(request, 'madadjoo/show_madadjoo_information.html',
                  {'user': user, 'hamyars': hamyars, 'needs': needs})


@admin_login_required
def admin_panel(request):
    if request.GET.get('success') == '1':
        print(request.user)
        return render(request, 'admin/admin_panel.html', {'success_message': request.user.first_name + ' ' +
                                                                             request.user.last_name + ' عزیز، شما با موفقیت وارد حساب کاربری خود شدید :)'})
    elif request.GET.get('success') == '3':
        return render(request, 'admin/admin_panel.html',
                      {'success_message': 'پیغام شما با موفقیت به همیاران ارسال شد.'})
    return render(request, 'admin/admin_panel.html')


@admin_login_required
def show_madadjoo_admin(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    all_madadjoo = madadjoo.objects.exclude(active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'admin/show_madadjoo.html', {'madadjoos': all_madadjoo})


@admin_login_required
def show_a_madadjoo_admin(request):
    target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
    needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
    hamyars = hamyar.objects.filter(sponsership__madadjoo_id=target_madadjoo.id)
    return render(request, 'admin/show_a_madadjoo.html',
                  {'user': target_madadjoo, 'needs': needs, 'hamyars': hamyars})


@admin_login_required
def edit_a_madadjoo_admin(request):
    if request.method == "GET":
        target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
        needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
        return render(request, 'admin/edit_madadjoo_full.html',
                      {'user': target_madadjoo, 'needs': needs})
    else:
        user = madadjoo.objects.get(username=request.GET.get('username', ''))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.id_number = request.POST.get('id_number')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        user.email = request.POST.get('email')
        user.bio = request.POST.get('bio')
        user.edu_status = request.POST.get('edu_status')
        user.successes = request.POST.get('successes')
        user.invest_percentage = request.POST.get('invest_percentage')
        if request.POST.get('profile_pic') != '':
            user.profile_pic = request.FILES.get('profile_pic')

        all_reqs = requirements.objects.filter(madadjoo_id=user.id)
        for req in all_reqs:
            prev_req = requirements.objects.get(id=req.id)
            prev_req.description = request.POST.get('description_base' + str(req.id))
            prev_req.cash = True if request.POST.get('cash_base' + str(req.id)) == "cash" else False
            prev_req.urgent = True if request.POST.get('urgent_base' + str(req.id)) == "urgent" else False
            prev_req.type = request.POST.get('type_base' + str(req.id))
            prev_req.confirmed = False if req.urgent else True
            prev_req.save()
            index = 0

        for desc in request.POST.getlist('description'):
            if desc != "":
                description = desc
                type = request.POST.get('type' + str(index))
                # print("hiiiiii")
                # print(desc)
                # print(type)
                cash = True if request.POST.get('cash' + str(index)) == "cash" else False
                urgent = True if request.POST.get('urgent' + str(index)) == "urgent" else False
                confirmed = False if urgent else True

                new_req = requirements(description=description, type=type, cash=cash, urgent=urgent,
                                       confirmed=confirmed, madadjoo_id=user.id)
                new_req.save()
            index += 1

        target_madadjoo = madadjoo.objects.get(username=request.GET.get('username', ''))
        needs = models.requirements.objects.filter(madadjoo_id=target_madadjoo.id)
        try:
            user.save()
            action.send(request.user, verb='به عنوان مدیر مشخصات مددجو را ویرایش کرد', target=target_madadjoo)
            s = 'اطلاعات مددجو با موفقیت ویرایش شد.'
            return render(request, 'admin/edit_madadjoo_full.html',
                          {'user': user, 'needs': needs, 'success_message': s})
        except IntegrityError:
            return render(request, 'admin/edit_madadjoo_full.html',
                          {'user': target_madadjoo, 'needs': needs, 'error_message': 'کد ملی باید یکتا باشد.'})


@admin_login_required
def inbox_admin(request):
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    add_madadjoo_letters = add_madadjoo_admin_letter.objects.all()
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)
    return render(request, 'admin/inbox.html',
                  {'add_madadjoo_letters': add_madadjoo_letters, 'madadjoo_letters': madadjoo_letters,
                   'urgent_need_letters': urgent_need_letters, 'change_madadkar_letters': change_madadkar_letters})


@admin_login_required
def confirm_madadjoo_admin(request):
    target_letter = models.add_madadjoo_admin_letter.objects.get(id=request.GET.get('letter', ''))
    add_madadjoo_letters = models.add_madadjoo_admin_letter.objects.all()
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    target_letter.madadjoo.confirmed = True
    target_letter.madadjoo.save()
    target_letter.delete()
    return render(request, 'admin/inbox.html',
                  {'madadjoo_letters': madadjoo_letters, 'change_madadkar_letters': change_madadkar_letters,
                   'add_madadjoo_letters': add_madadjoo_letters, 'urgent_need_letters': urgent_need_letters,
                   'success_message': "مددجوی انتخابی تایید شد."})


@admin_login_required
def confirm_need_admin(request):
    target_letter = models.urgent_need_admin_letter.objects.get(id=request.GET.get('letter', ''))
    add_madadjoo_letters = models.add_madadjoo_admin_letter.objects.all()
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    target_letter.need.urgent = True
    target_letter.need.save()
    action.send(request.user, verb='ثبت نیاز فوری برای مددجو', target=target_letter.madadjoo)
    target_letter.delete()
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)

    return render(request, 'admin/inbox.html',
                  {'madadjoo_letters': madadjoo_letters, 'change_madadkar_letters': change_madadkar_letters,
                   'add_madadjoo_letters': add_madadjoo_letters, 'urgent_need_letters': urgent_need_letters,
                   'success_message': "نیاز فوری انتخابی تایید شد."})


@admin_login_required
def confirm_change_madadkar(request):
    target_letter = models.request_for_change_madadkar.objects.get(id=request.GET.get('letter', ''))
    add_madadjoo_letters = models.add_madadjoo_admin_letter.objects.all()
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)
    target_letter.madadjoo.corr_madadkar = None
    target_letter.madadjoo.save()
    target_letter.confirmed = True
    target_letter.save()
    action.send(request.user, verb='درخواست تغییر مدکار توسط مددجو', target=target_letter.madadjoo)

    return render(request, 'admin/inbox.html',
                  {'madadjoo_letters': madadjoo_letters, 'change_madadkar_letters': change_madadkar_letters,
                   'add_madadjoo_letters': add_madadjoo_letters, 'urgent_need_letters': urgent_need_letters,
                   'success_message': "درخواست تغییر مددکار تایید شد."})


@admin_login_required
def letter_madadkar_add_madadjoo(request):
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    target_letter = models.add_madadjoo_admin_letter.objects.get(id=request.GET.get('letter', ''))
    add_madadjoo_letters = models.add_madadjoo_admin_letter.objects.all()
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    return render(request, 'admin/letter_content_confirm.html',
                  {'letter': target_letter, 'add_madadjoo_letters': add_madadjoo_letters,
                   'urgent_need_letters': urgent_need_letters, 'change_madadkar_letters': change_madadkar_letters,
                   'madadjoo_letters': madadjoo_letters})


@admin_login_required
def urgent_need_letters(request):
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    target_letter = models.urgent_need_admin_letter.objects.get(id=request.GET.get('letter', ''))
    add_madadjoo_letters = models.add_madadjoo_admin_letter.objects.all()
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    return render(request, 'admin/letter_content_urgent.html',
                  {'letter': target_letter, 'add_madadjoo_letters': add_madadjoo_letters,
                   'urgent_need_letters': urgent_need_letters, 'change_madadkar_letters': change_madadkar_letters,
                   'madadjoo_letters': madadjoo_letters})


@admin_login_required
def change_madadkar_letters(request):
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    target_letter = models.request_for_change_madadkar.objects.get(id=request.GET.get('letter', ''))
    add_madadjoo_letters = models.add_madadjoo_admin_letter.objects.all()
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    return render(request, 'admin/letter_content_change_madadkar.html',
                  {'letter': target_letter, 'add_madadjoo_letters': add_madadjoo_letters,
                   'urgent_need_letters': urgent_need_letters, 'change_madadkar_letters': change_madadkar_letters,
                   'madadjoo_letters': madadjoo_letters})


@admin_login_required
def madadjoo_letters_admin(request):
    admin_as_a_madadkar = madadkar.objects.get(id=request.user.id)
    target_letter = models.madadjoo_madadkar_letter.objects.get(id=request.GET.get('letter', ''))
    add_madadjoo_letters = models.add_madadjoo_admin_letter.objects.all()
    urgent_need_letters = urgent_need_admin_letter.objects.all()
    madadjoo_letters = madadjoo_madadkar_letter.objects.filter(madadkar=admin_as_a_madadkar)
    change_madadkar_letters = request_for_change_madadkar.objects.filter(confirmed=False)
    return render(request, 'admin/letter_content_madadjoo.html',
                  {'letter': target_letter, 'add_madadjoo_letters': add_madadjoo_letters, 'change_madadkar_letters': change_madadkar_letters,
                   'urgent_need_letters': urgent_need_letters, 'madadjoo_letters': madadjoo_letters})


@admin_login_required
def warning_letter_admin(request):
    target_madadkar = madadkar.objects.get(username=request.GET.get('username', ''))
    user = admin_user.objects.get(username=request.user.username)
    new_warning = warning_admin_letter(admin_user=user, madadkar=target_madadkar)
    try:
        new_warning.save()
        return render(request, 'admin/edit_a_madadkar.html', {'madadkar': target_madadkar,
                                                              'warning_message': 'اخطار به این مددکار ارسال شد'})
    except IntegrityError:
        return render(request, 'admin/edit_a_madadkar.html',
                      {'madadkar': target_madadkar,
                       'error_message': 'متاسفانه امکان ارسال اخطار به این مددکار وجود ندارد'})


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
        profile_pic = request.FILES.get('profile_pic')
        bio = request.POST.get('bio')
        edu_status = request.POST.get('edu_status')
        successes = request.POST.get('successes')

        invest_percentage = request.POST.get('invest_percentage')
        invest_percentage = '0.0' if invest_percentage == '' else invest_percentage
        description = request.POST.get('description')
        type = request.POST.get('type')
        corr_madadkar = madadkar.objects.get(username=request.user.username)
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
                                      {"error_message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError:
            return render_to_response("admin/add_a_madadjoo.html", {"error_message": "لطفا موارد الزامی را تکمیل کنید"})

        # return HttpResponseRedirect(reverse("admin_panel"))
        return render(request, 'admin/add_a_madadjoo.html',
                      {'success_message': 'مددجوی جدید با موفقیت در سامانه ثبت گردید.'})


@madadkar_login_required
@csrf_exempt
def add_a_madadjoo_madadkar(request):
    if request.method == "GET":
        return render(request, 'madadkar/add_a_madadjoo.html')
    else:
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        phone_number = request.POST.get('phone_number')
        phone_number = '0' if phone_number == '' else phone_number
        address = request.POST.get('address')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        # print(profile_pic)
        bio = request.POST.get('bio')
        edu_status = request.POST.get('edu_status')
        successes = request.POST.get('successes')

        invest_percentage = request.POST.get('invest_percentage')
        invest_percentage = '0.0' if invest_percentage == '' else invest_percentage
        description = request.POST.get('description')
        type = request.POST.get('type')

        id_madadkar = models.active_user.objects.get(username=request.user).id
        corr_madadkar = models.madadkar.objects.get(active_user_ptr_id=id_madadkar)

        new_madadjoo = models.madadjoo(username=username, first_name=first_name,
                                       last_name=last_name, id_number=id_number, phone_number=phone_number,
                                       address=address, email=email, profile_pic=profile_pic, bio=bio,
                                       edu_status=edu_status, successes=successes, removed=False,
                                       invest_percentage=invest_percentage, corr_madadkar=corr_madadkar,
                                       confirmed=False,
                                       )
        new_madadjoo.set_password(request.POST.get("password"))
        warning_message = False
        try:
            new_madadjoo.save()
            letter = add_madadjoo_admin_letter(madadjoo=new_madadjoo, madadkar=corr_madadkar,
                                               text="درخواست تایید مددجو را دارم.")
            letter.save()
            index = 0
            for desc in request.POST.getlist('description'):
                if desc != "":
                    description = desc
                    type = request.POST.get('type' + str(index))
                    cash = True if request.POST.get('cash' + str(index)) == "cash" else False
                    urgent = True if request.POST.get('urgent' + str(index)) == "urgent" else False
                    confirmed = False if urgent else True

                    new_req = requirements(description=description, type=type, cash=cash, urgent=urgent,
                                           confirmed=confirmed, madadjoo_id=new_madadjoo.id)
                    new_req.save()

                    if urgent:
                        warning_message = True
                        new_urgent = urgent_need_admin_letter(madadkar=corr_madadkar, madadjoo=new_madadjoo,
                                                              need=new_req)
                        new_urgent.save()
                        new_req.urgent = False
                        new_req.save()

                index += 1

        except IntegrityError:
            return render_to_response("madadkar/add_a_madadjoo.html",
                                      {"error_message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError:
            return render_to_response("madadkar/add_a_madadjoo.html",
                                      {"error_message": "لطفا موارد الزامی را تکمیل کنید"})

        if warning_message:
            w = 'نیاز‌/نیاز‌های فوری ثبت شده بعد از تایید مدیر نهایی خواهند شد'
            return render(request, 'madadkar/add_a_madadjoo.html',
                          {'success_message': 'مددجوی جدید برای تایید به مدیر سامانه ارسال گردید.',
                           'warning_message': w})
        action.send(request.user, verb="مددجوی جدیدی را وارد سامانه کرد", target=new_madadjoo)
        return render(request, 'madadkar/add_a_madadjoo.html',
                      {'success_message': 'مددجوی جدید برای تایید به مدیر سامانه ارسال گردید.'})


@admin_login_required
def show_madadkar_admin(request):
    madadkars = madadkar.objects.all()
    return render(request, 'admin/show_madadkar.html', {'hamyars': madadkars})


@admin_login_required
def show_a_madadkar_admin(request):
    target_madadkar = madadkar.objects.get(username=request.GET.get('username', ''))
    madadjoos = madadjoo.objects.filter(corr_madadkar=target_madadkar)
    return render(request, 'admin/show_a_madadkar.html', {'madadkar': target_madadkar})


@admin_login_required
def edit_a_madadkar_admin(request):
    target_madadkar = madadkar.objects.get(username=request.GET.get('username', ''))
    if request.method == "GET":
        return render(request, 'admin/edit_a_madadkar.html', {'madadkar': target_madadkar})
    else:

        target_madadkar.first_name = request.POST.get('first_name')
        target_madadkar.last_name = request.POST.get('last_name')
        target_madadkar.id_number = request.POST.get('id_number')
        target_madadkar.phone_number = request.POST.get('phone_number')
        target_madadkar.address = request.POST.get('address')
        target_madadkar.email = request.POST.get('email')
        target_madadkar.bio = request.POST.get('bio')

        if request.POST.get('profile_pic') != '':
            target_madadkar.profile_pic = request.FILES.get('profile_pic')
        try:
            target_madadkar.save()
            return render(request, 'admin/edit_a_madadkar.html', {'madadkar': target_madadkar,
                                                                  'success_message': 'اطلاعات شما با موفقیت ویرایش شد.'})
        except IntegrityError:
            return render(request, 'admin/edit_a_madadkar.html',
                          {'madadkar': target_madadkar, 'error_message': 'کد ملی باید یکتا باشد.'})


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
        profile_pic = request.FILES.get('profile_pic')
        bio = request.POST.get('bio')

        new_madadkar = models.madadkar(username=username, first_name=first_name,
                                       last_name=last_name, id_number=id_number, phone_number=phone_number,
                                       address=address, email=email, profile_pic=profile_pic, bio=bio)
        new_madadkar.set_password(request.POST.get("password"))
        try:
            new_madadkar.save()
        except IntegrityError:
            return render_to_response("admin/add_a_madadkar.html",
                                      {"error_message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError:
            return render_to_response("admin/add_a_madadkar.html", {"error_message": "لطفا موارد الزامی را تکمیل کنید"})

        # return HttpResponseRedirect(reverse("admin_panel"))
        return render(request, 'admin/add_a_madadkar.html',
                      {'success_message': 'مددکار جدید با موفقیت در سامانه ثبت گردید.'})


@admin_login_required
def show_hamyar_admin(request):
    all_hamyars = hamyar.objects.all()
    return render(request, 'admin/show_hamyar.html', {'hamyars': all_hamyars})


@admin_login_required
def show_a_hamyar_admin(request):
    target_hamyar = hamyar.objects.get(username=request.GET.get('username', ''))
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    madadjoos = madadjoo.objects.filter(sponsership__hamyar=target_hamyar).exclude(
        active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'admin/show_a_hamyar.html', {'hamyar': target_hamyar, 'madadjoos': madadjoos})


@admin_login_required
def edit_a_hamyar_admin(request):
    target_hamyar = hamyar.objects.get(username=request.GET.get('username', ''))
    if request.method == "GET":
        return render(request, 'admin/edit_a_hamyar.html', {'hamyar': target_hamyar})
    else:

        target_hamyar.first_name = request.POST.get('first_name')
        target_hamyar.last_name = request.POST.get('last_name')
        target_hamyar.id_number = request.POST.get('id_number')
        target_hamyar.phone_number = request.POST.get('phone_number')
        target_hamyar.address = request.POST.get('address')
        target_hamyar.email = request.POST.get('email')

        if request.POST.get('profile_pic') != '':
            target_hamyar.profile_pic = request.FILES.get('profile_pic')
        try:
            target_hamyar.save()
            return render(request, 'admin/edit_a_hamyar.html', {'hamyar': target_hamyar,
                                                                'success_message': 'اطلاعات شما با موفقیت ویرایش شد.'})
        except IntegrityError:
            return render(request, 'admin/edit_a_hamyar.html',
                          {'hamyar': target_hamyar, 'error_message': 'کد ملی باید یکتا باشد.'})


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
        profile_pic = request.FILES.get('profile_pic')

        new_madadkar = models.hamyar(username=username, first_name=first_name,
                                     last_name=last_name, id_number=id_number, phone_number=phone_number,
                                     address=address, email=email, profile_pic=profile_pic)
        new_madadkar.set_password(request.POST.get("password"))
        try:
            new_madadkar.save()
        except IntegrityError:
            return render_to_response("admin/add_a_hamyar.html",
                                      {"error_message": "این نام کاربری یا کد ملی قبلا انتخاب شده است"})
        except ValueError:
            return render_to_response("admin/add_a_hamyar.html", {"error_message": "لطفا موارد الزامی را تکمیل کنید"})

        # return HttpResponseRedirect(reverse("admin_panel"))
        return render(request, 'admin/add_a_hamyar.html',
                      {'success_message': 'همیار جدید با موفقیت در سامانه ثبت گردید.'})


@admin_login_required
def payment_reports_admin(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    cash = hamyar_madadjoo_payment.objects.exclude(madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    non_cash = hamyar_madadjoo_non_cash.objects.exclude(madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    system = hamyar_system_payment.objects.all()

    cash_for_deleteds = hamyar_madadjoo_payment.objects.filter(madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    non_cash_for_deleteds = hamyar_madadjoo_non_cash.objects.filter(madadjoo__active_user_ptr_id__in=deleted_madadjoos)
    return render(request, 'admin/payment_reports.html', {'cash': cash, 'non_cash': non_cash,
                                                          'system': system,
                                                          'cash_for_deleteds': cash_for_deleteds,
                                                          'non_cash_for_deleteds': non_cash_for_deleteds})


@admin_login_required
def activity_report(request):
    madadjoo_stream = []
    for target_madadjoo in madadjoo.objects.all():
        madadjoo_stream.append((target_madadjoo, target_stream(target_madadjoo)))

    hamyar_ids = hamyar.objects.values('id')
    madadkar_ids = madadkar.objects.values('id')

    hamyar_stream = []
    for target_hamyar in active_user.objects.filter(hamyar__active_user_ptr_id__in=hamyar_ids):
        hamyar_stream.append((target_hamyar, actor_stream(target_hamyar)))

    madadkar_stream = []
    for target_madadkar in active_user.objects.filter(madadkar__active_user_ptr_id__in=madadkar_ids):
        madadkar_stream.append((target_madadkar, actor_stream(target_madadkar)))
    return render(request, 'admin/activity_reports.html',
                  {'madadjoo_stream': madadjoo_stream, 'hamyar_stream': hamyar_stream,
                   'madadkar_stream': madadkar_stream})


@admin_login_required
def madadjoo_paid_report(request):
    return render(request, 'admin/madadjoo_paid_report.html')


@admin_login_required
def need_report_admin(request):
    deleted_madadjoos = madadkar_remove_madadjoo.objects.values('madadjoo_id')
    paid_needs = hamyar_madadjoo_payment.objects.values('need_id')

    unpaid_needs = []

    for target_madadjoo in madadjoo.objects.exclude(active_user_ptr_id__in=deleted_madadjoos):
        target_needs = requirements.objects.filter(madadjoo=target_madadjoo).exclude(id__in=paid_needs)
        if len(target_needs) > 0:
            unpaid_needs.append(
                (target_madadjoo, target_needs))

    return render(request, 'admin/need_report.html', {'unpaid_needs': unpaid_needs})
