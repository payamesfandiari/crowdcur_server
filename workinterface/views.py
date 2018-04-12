from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'workinterface/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.all()[:5]


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