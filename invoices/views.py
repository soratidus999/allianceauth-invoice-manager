import os
from allianceauth.eveonline.evelinks.eveimageserver import corporation_logo_url

from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from .app_settings import PAYMENT_CORP
from allianceauth.eveonline.models import EveCorporationInfo
from esi.decorators import token_required
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from .models import Invoice

@login_required
def show_invoices(request):
    try:
        recipt_corp = EveCorporationInfo.objects.get(corporation_id=PAYMENT_CORP)
    except:
        recipt_corp = "None"
    chars = request.user.character_ownerships.all().values_list('character')
    admin_invoices = Invoice.objects.visible_to(request.user).filter(paid=False).exclude(character__in=chars)
    invoices = Invoice.objects.visible_to(request.user).filter(paid=False, character__in=chars)
    outstanding_isk = invoices.aggregate(total_isk=Sum('amount'))
    admin_isk = admin_invoices.aggregate(total_isk=Sum('amount'))
    completed_invoices = Invoice.objects.visible_to(request.user).filter(paid=True, character__in=chars).order_by('-due_date')[:10]
    if outstanding_isk['total_isk'] == None:
        outstanding = 0
    else:
        outstanding = outstanding_isk['total_isk']

    ctx = { 'invoices':invoices, 
            'admin_invoices':admin_invoices,
            'admin_isk': admin_isk['total_isk'],
            'outstanding_isk': outstanding,
            'complete_invoices':completed_invoices,
            'recipt_corp':recipt_corp}

    return render(request, 'invoices/list.html', context=ctx)

@login_required
@permission_required('invoices.admin')
def admin_create_tasks(request):
    schedule_check_payments, _ = CrontabSchedule.objects.get_or_create(minute='15,30,45',
                                                             hour='*',
                                                             day_of_week='*',
                                                             day_of_month='*',
                                                             month_of_year='*',
                                                             timezone='UTC'
                                                             )

    schedule_outstanding_payments, _ = CrontabSchedule.objects.get_or_create(minute='0',
                                                             hour='12',
                                                             day_of_week='*',
                                                             day_of_month='*',
                                                             month_of_year='*',
                                                             timezone='UTC'
                                                             )

    task_check_payments = PeriodicTask.objects.update_or_create(
        task='invoices.tasks.check_for_payments',
        defaults={
            'crontab': schedule_check_payments,
            'name': 'Check For Invoice Putstanding Payments',
            'enabled': True
        }
    )
    # Lets check every 15Mins
    task_outstanding_payments = PeriodicTask.objects.update_or_create(
        task='invoices.tasks.check_for_outstanding',
        defaults={
            'crontab': schedule_outstanding_payments,
            'name': 'Check For ESI Payments made',
            'enabled': True
        }
    )

    messages.info(
        request, "Created/Reset Invoice Task to defaults")

    return redirect('invoices:list')
