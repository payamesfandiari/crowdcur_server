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


@login_required
def log_worker_answer(request,task_uid):
    task = get_object_or_404(Task, task_uid=task_uid)
    history = WorkerTaskHistoryModel(task=task, worker=request.user)
    history.save()
    tasks.check_needs_update(request.user)
    # I should send three variables to Kavan.
    return JsonResponse({"response" : 1})


