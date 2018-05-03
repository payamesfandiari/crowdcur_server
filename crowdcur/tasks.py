import pandas as pd
import numpy as np
from background_task import background
from logging import getLogger
from django.shortcuts import get_object_or_404, render
from estimators.models import Estimator
from sklearn.linear_model import LinearRegression

from .models import (WorkerPreferenceHistoryModel,
                     WorkerTaskHistoryModel,
                     WorkerModel,
                     TaskFeaturesModel,
                     WorkerKFactor,
                     PreferenceToFeaturesModel)

logger = getLogger(__name__)


def check_needs_update(worker):
    if WorkerModel.objects.filter(worker=worker).exists():
        worker_model = WorkerModel.objects.get(worker=worker)
        if worker_model.needs_update:
            worker_model.needs_update = False
            worker_model.save()
            update_worker_model(worker.id)
    else:
        est = LinearRegression()
        model = Estimator(estimator = est)
        model.description = "worker model of %s" % worker.username
        model.save()
        worker_model = WorkerModel(worker=worker,worker_model=model)
        worker_model.needs_update = False
        worker_model.save()
        update_worker_model(worker.id)


@background(schedule=1)
def update_worker_model(worker_id):
    model = WorkerModel.objects.get(worker_id=worker_id)
    current_factors_model,created = WorkerKFactor.objects.get_or_create(worker_id=worker_id)
    if created:
        current_factors_model.factors = {}
        current_factors_model.save()
    else:
        current_factors = current_factors_model.factors
        new_factors_model = WorkerPreferenceHistoryModel.objects.filter(worker_id=worker_id).latest('timestamp')
        new_factors = new_factors_model.preference
    worker_history = WorkerTaskHistoryModel.objects.filter(worker_id=worker_id).values('task', 'time_it_took', 'successful')
    X = np.array(list(
        TaskFeaturesModel.objects.filter(
            task_id__in=worker_history.values_list('task', flat=True)).values_list('task_feature', flat=True)))
    y = np.array(worker_history.values_list('time_it_took',flat=True))
    print('Something will happen next',X.shape)
    return True