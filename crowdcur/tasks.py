import pandas as pd
import numpy as np
from background_task import background
from logging import getLogger
from efp_learner.worker_model import WorkerModel as wm
from .models import (WorkerPreferenceHistoryModel,
                     WorkerTaskHistoryModel,
                     WorkerModel,
                     TaskFeaturesModel,
                     TaskFeatureMapping)

logger = getLogger(__name__)


def check_needs_update(worker):
    if WorkerModel.objects.filter(worker=worker).exists():
        worker_model = WorkerModel.objects.get(worker=worker)
        if worker_model.needs_update:
            update_worker_model(worker.id)
    else:
        worker_model = WorkerModel(worker=worker)
        worker_model.save()
        update_worker_model(worker.id)


@background(schedule=1)
def update_worker_model(worker_id):
    model = WorkerModel.objects.get(worker_id=worker_id)
    columns = {t['feature_name']:t['col_number'] for t in TaskFeatureMapping.objects.values()}
    worker_history = WorkerTaskHistoryModel.objects.filter(
        worker_id=worker_id,successful=True).order_by('-timestamp')[:15].values('task', 'time_it_took')
    if worker_history.count() < 5:
        return False
    try:
        worker_latest_pref = WorkerPreferenceHistoryModel.objects.filter(worker_id=worker_id).latest('timestamp').preference
    except WorkerPreferenceHistoryModel.DoesNotExist:
        worker_latest_pref = None
    X = pd.DataFrame(list(
        TaskFeaturesModel.objects.filter(
            task_id__in=worker_history.values_list('task', flat=True)).values_list('feature', flat=True)))
    y = np.array(worker_history.values_list('time_it_took',flat=True))
    clf = wm()
    clf.columns = columns
    if len(worker_latest_pref) > 1:
        clf.preferences = worker_latest_pref
    clf.fit(X,y)
    model.worker_model = clf.get_factor_scores()
    model.score = clf.get_loss(X, y)
    model.needs_update = False
    model.save()
    return True

