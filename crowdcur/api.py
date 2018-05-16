from .models import *
from accounts.models import User
from workinterface.models import Task
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Avg, Count, Min, Sum, Q, F, StdDev
import random


def color_gen():
    return 'rgb(%s,%s,%s)' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_time_spent(request):
    worker = request.user
    history = WorkerTaskHistoryModel.objects.filter(worker=worker, successful=True).values('task__task_type',
                                                                                           'task__task_type__task_title').order_by(
        'task__task_type').annotate(time_spent=Sum('time_it_took'))
    overall_time = \
    WorkerTaskHistoryModel.objects.filter(worker=worker, successful=True).aggregate(overall_time=Sum('time_it_took'))[
        'overall_time']
    out = {'res': 1, 'datasets': [{'data':[],'backgroundColor':[]}], 'labels': []}
    if history.count() < 1:
        return JsonResponse({'res': 0})
    for t in history:
        out['labels'].append(t['task__task_type__task_title'])
        out['datasets'][0]['data'].append(100 * (t['time_spent'] / overall_time))
        out['datasets'][0]['backgroundColor'].append(color_gen())

    return JsonResponse(out)


def get_pref_change(request):
    worker = request.user
    model_history = WorkerModelHistoryModel.objects.filter(worker=worker).values('worker_model','timestamp').order_by('timestamp')

    return None



def get_demographics(request):
    out = {
        'prof': 12,
        'adjunct_prof': 34,
        'phd': 123,
        'ms': 21,
        'bs': 10,
    }
    return JsonResponse(out)


def get_most_worked_on(request):
    out = {
        'values': [19, 26, 55],
    }

#
# def get_avg_time(request,username):
#     return JsonResponse({'username':username,'avg_time':15.2})
#
# def get_avg_money(request,username):
#     return JsonResponse({'username': username, 'avg_money': 0.32})
#
# def get_avg_accuracy(request,username):
#     return JsonResponse({'username': username, 'avg_acc': 98.2})
#
# def get_total_time(request,username):
#     return JsonResponse({'username':username,'total_time':1523.12})
#
