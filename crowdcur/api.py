from django.shortcuts import render
from .models import WorkerPreferenceHistoryModel,WorkerTaskHistoryModel,WorkerModel,TaskFeaturesModel
from accounts.models import User
from workinterface.models import Task
# Create your views here.
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
import json
from . import tasks

def get_info(request):
    out = {
        'username' : request.user.username,
        'avg_time': 15.2,
        'avg_money': 0.32,
        'avg_acc': 98.2,
        'total_time': 1523.12
    }
    return JsonResponse(out)


def get_demographics(request):
    out = {
        'prof' : 12,
        'adjunct_prof' : 34,
        'phd' : 123,
        'ms' : 21,
        'bs' : 10,
    }
    return JsonResponse(out)


def get_pref_change(request):
    pass


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
