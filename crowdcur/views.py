from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WorkerPreferenceHistoryModel, WorkerTaskHistoryModel, WorkerModel, TaskFeaturesModel,PreferenceToFeaturesModel
from accounts.models import User
from workinterface.models import Task
# Create your views here.
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
from . import tasks


@login_required
def log_worker_answer(request):
    if request.is_ajax():
        worker = request.user
        task_uid = request.GET.get('task_uid',None)
        time_it_took = request.GET.get('time_took', 0)
        task = get_object_or_404(Task, task_uid=task_uid)
        history,created = WorkerTaskHistoryModel.objects.get_or_create(task=task,worker=worker)
        history.successful = True
        history.time_it_took = time_it_took
        history.save()
        tasks.check_needs_update(request.user)
    # I should send three variables to Kavan.
    return JsonResponse({"response": 1})


@login_required
def set_worker_shown_tasks(request):
    if request.is_ajax():
        worker = request.user
        tasks = request.POST.get('tasks',None)
        if tasks is not None:
            tasks = tasks.split(',')
            for t_uid in tasks:
                task = Task.objects.get(task_uid=t_uid)
                t,created = WorkerTaskHistoryModel.objects.get_or_create(task=task,worker=worker)
                t.save()

    return JsonResponse({"response":1})


def get_info(request):
    return JsonResponse({"response": 1,"MoneyMade":1523.12,"AvgDuration":15.2})


class WorkerDashboardView(generic.TemplateView):
    template_name = 'crowdcur/worker_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(WorkerDashboardView, self).get_context_data(**kwargs)
        context['username'] = 'Payam'
        context['info'] = {'avg_time': 15.2,
                           'avg_money': 0.32,
                           'avg_acc': 98.2,
                           'total_time': 1523.12,
                           'total_money': 1523.12,
                           }
        return context


class WorkerFeedbackView(LoginRequiredMixin,generic.TemplateView):
    template_name = "crowdcur/feedback.html"

    def post(self,request,*args,**kwargs):
        if self.request.is_ajax():
            worker = self.request.user
            pref = dict(self.request.POST)["worker_pref[]"]
            pref_model = WorkerPreferenceHistoryModel(worker=worker)
            if pref is not None:
                pref_model.preference={u:i for i,u in enumerate(pref)}
            pref_model.save()
            worker_model = WorkerModel.objects.get(worker=worker)
            worker_model.needs_update = True
            worker_model.save()
            tasks.check_needs_update(worker)
            return JsonResponse({"response":1})
        else:
            return JsonResponse({"response": 0})


