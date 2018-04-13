from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from random import sample
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
    return HttpResponseRedirect(reverse('index'))


class IndexView(LoginRequiredMixin,generic.ListView):
    login_url = '/accounts/login/'
    template_name = 'workinterface/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        worker = self.request.user
        t = Task.objects.exclude(pk__in=Answers.objects.filter(worker=worker).values_list('task', flat=True))
        jobs = Job.objects.values_list('id', flat=True)
        s = []
        for j in jobs:
            s.extend(sample(list(t.filter(task_type=j).values_list('id', flat=True)), 5))
        if len(s) > 10:
            s = sample(s, 10)

        return t.filter(pk__in=s)


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