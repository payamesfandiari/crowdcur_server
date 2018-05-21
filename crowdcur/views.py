from random import randint
from operator import itemgetter
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WorkerPreferenceHistoryModel, WorkerTaskHistoryModel, WorkerModel
from workinterface.models import Task
# Create your views here.
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from . import tasks
from accounts.models import User


@login_required
def log_worker_answer(request):
    if request.is_ajax():
        worker = request.user
        task_uid = request.GET.get('task_uid', None)
        time_it_took = request.GET.get('time_took', 0)
        task = get_object_or_404(Task, task_uid=task_uid)
        history, created = WorkerTaskHistoryModel.objects.get_or_create(task=task, worker=worker)
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
        tasks = request.POST.get('tasks', None)
        if tasks is not None:
            tasks = tasks.split(',')
            for t_uid in tasks:
                task = Task.objects.get(task_uid=t_uid)
                t, created = WorkerTaskHistoryModel.objects.get_or_create(task=task, worker=worker)
                t.save()

    return JsonResponse({"response": 1})


def get_info(request):
    worker_info = \
        User.worker_info(request.user.username).values('completed_task', 'success_task', 'average_income', 'sum_income',
                                                       'sum_duration',
                                                       'avg_duration')[0]
    return JsonResponse({"response": 1,
                         "money_made": worker_info['sum_income'],
                         "avg_duration": worker_info['sum_duration'],
                         "tasks_seen": worker_info['completed_task'],
                         "tasks_comp": worker_info['success_task'],
                         "username": request.user.username
                         })


class WorkerDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'crowdcur/worker_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(WorkerDashboardView, self).get_context_data(**kwargs)

        context['username'] = self.request.user.username
        worker_info = User.worker_info(self.request.user.username)
        context['info'] = \
            worker_info.values('completed_task', 'success_task', 'average_income', 'sum_income', 'sum_duration',
                               'avg_duration')[0]
        return context


class WorkerFeedbackView(LoginRequiredMixin, generic.TemplateView):
    template_name = "crowdcur/feedback.html"

    def get_context_data(self, **kwargs):
        context = super(WorkerFeedbackView, self).get_context_data()
        worker = self.request.user
        worker_model = WorkerModel.objects.get(worker=worker)
        if worker_model.needs_update:
            pref = worker.preference
        else:
            factor_scores = sorted(worker_model.worker_model.items(), key=itemgetter(1), reverse=True)[:5]
            pref = [u for u, v in factor_scores]
        context['pref'] = pref
        return context

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            worker = self.request.user
            pref = dict(self.request.POST)["worker_pref[]"]
            pref_model = WorkerPreferenceHistoryModel(worker=worker)
            if pref is not None:
                pref_model.preference = {u: i for i, u in enumerate(pref)}
            pref_model.save()
            worker_model = WorkerModel.objects.get(worker=worker)
            worker_model.needs_update = True
            worker_model.save()
            tasks.check_needs_update(worker)
            return JsonResponse({"response": 1})
        else:
            return JsonResponse({"response": 0})


@login_required
def get_time_spent(request):
    out = {
        'labels': ['tweet analysis', 'sentiment analysis', 'tweet classification', 'image', 'image labeling'],
        'data': [randint(10, 100) for u in range(5)]
    }
    return JsonResponse(out)


@login_required
def get_task_type(request):
    out = {
        'labels': ['tweet analysis', 'sentiment analysis', 'tweet classification', 'image', 'image labeling'],
        'data': [randint(10, 100) for u in range(5)]
    }
    return JsonResponse(out)


@login_required
def get_income(request):
    out = {
        'labels': ['tweet analysis', 'sentiment analysis', 'tweet classification', 'image', 'image labeling'],
        'data': [randint(10, 100) for u in range(5)]
    }
    return JsonResponse(out)


@login_required
def get_accuracy(request):
    out = {
        'labels': ['tweet analysis', 'sentiment analysis', 'tweet classification', 'image', 'image labeling'],
        'data': [randint(10, 100) for u in range(5)]
    }
    return JsonResponse(out)
