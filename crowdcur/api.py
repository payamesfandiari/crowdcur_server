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


