from background_task import background
from logging import getLogger
from django.shortcuts import get_object_or_404, render
from .models import WorkerPreferenceHistoryModel,WorkerTaskHistoryModel,WorkerModel,TaskFeaturesModel

logger = getLogger(__name__)


def check_needs_update(worker):
    worker_model = WorkerModel.objects.get(worker=worker)
    if worker_model.needs_update:
        update_worker_model(worker)


@background(schedule=1)
def update_worker_model(worker_id):
    logger.info("We will update the worker model for the specific worker {0}".format(worker_id))


