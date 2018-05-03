from collections import Counter
from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from .models import *
from django.db.models import Min, Max, Count, F, Avg, Sum

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


class OverviewWorker:
    def __init__(self, filters,worker):
        self._filters = filters
        self.task_history = WorkerTaskHistoryModel.objects.filter(worker=worker)
        self.pref_history = WorkerPreferenceHistoryModel.objects.filter(worker=worker)

        self.bounds = self.task_history.aggregate(min_time=Min('timestamp'),max_time=Max('timestamp'))
        if self.bounds['max_time'] and self.bounds['min_time']:
            self.span = self.bounds['max_time'] - self.bounds['min_time']
        else:
            self.span = timedelta(0, 0)

    def precision(self):
        if self.span >= timedelta(days=365):
            return 'month'
        elif self.span >= timedelta(days=7):
            return 'day'
        else:
            return 'hour'

    def avg_time(self):
        results = self.task_history.aggregate(Avg('time_it_took'))
        return list(results)

    def avg_money(self):
        results = self.task_history.aggregate(money_made=Sum('task__task_type__task_payment'))
        return list(results)

    def max_min_money(self):
        results = self.task_history.aggregate(max_money_made=Max('task__task_type__task_payment'),
                                              min_money_made=Min('task__task_type__task_payment'))
        return list(results)

    def preference_change(self):
        results = self.pref_history.order_by('-timestamp')
        out = {}
        return out




    def to_dict(self):
        return {
            'filter': self._filters,
            'bounds': self.bounds,

        }