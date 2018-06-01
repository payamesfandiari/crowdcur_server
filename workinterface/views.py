from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from random import sample,shuffle,randint
from django.db.models import Max
from django.views import generic
# Create your views here.
import json
from .models import *



@login_required
def ans(request,pk):
    task = get_object_or_404(Task,pk=pk)
    content = json.dumps(request.POST['ans'])
    ans = Answers(task=task,worker=request.user,content=content)
    ans.save()
    AssignedTaskSet.objects.filter(worker=request.user,tasks=task).update(is_done=True)
    return HttpResponseRedirect(reverse('work'))


@login_required
def refresh_workspace(request):
    AssignedTaskSet.objects.filter(worker=request.user,is_done=False).delete()
    return HttpResponseRedirect(reverse('work'))


class IndexView(LoginRequiredMixin,generic.ListView):
    login_url = '/accounts/login/'
    template_name = 'workinterface/work.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        worker = self.request.user
        assigned_tasks = AssignedTaskSet.objects.filter(worker=worker,is_done=False).count()
        if assigned_tasks == 0:
            t = Task.objects.exclude(pk__in=Answers.objects.filter(worker=worker).values_list('task', flat=True))
            jobs = Job.objects.values_list('id', flat=True)
            s = []
            for j in jobs:
                s.extend(sample(list(t.filter(task_type=j).values_list('id', flat=True)), 5))
            if len(s) > 10:
                s = sample(s, 10)
            for task in s:
                AssignedTaskSet.objects.create(worker=worker,tasks_id=task)
            return t.filter(pk__in=s)
        elif assigned_tasks < 10:
            max_id = Task.objects.all().aggregate(max_id=Max("id"))['max_id']
            num_tasks_to_be_added = 10 - assigned_tasks
            pks = []
            for i in range(num_tasks_to_be_added):
                pk = randint(1, max_id)
                if pk not in pks:
                    pks.append(pk)

            for task in pks:
                AssignedTaskSet.objects.create(worker=worker, tasks_id=task)
            return Task.objects.filter(pk__in=AssignedTaskSet.objects.filter(worker=worker,is_done=False).values_list('tasks_id'))

        return Task.objects.filter(
                pk__in=AssignedTaskSet.objects.filter(worker=worker, is_done=False).values_list('tasks_id'))

    def get_context_data(self, *, object_list=None, **kwargs):
        NUM_IN_EACH_ROW = 5
        context = super(IndexView,self).get_context_data(**kwargs)
        num_of_tasks = len(context['tasks'])
        tasks = list(context['tasks'])
        shuffle(tasks)
        temp = []
        for i in range(0,num_of_tasks,NUM_IN_EACH_ROW):
            temp.append(tasks[i:i+NUM_IN_EACH_ROW])
        context['tasks'] = temp
        return context


class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Task
    template_name = 'workinterface/answer.html'
    context_object_name = 'task'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        d = json.loads(self.object.task_content)
        context['t'] = d
        return context