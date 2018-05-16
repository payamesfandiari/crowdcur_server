
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WorkerModel,WorkerModelHistoryModel


@receiver(post_save,sender=WorkerModel)
def push_worker_model_history(sender, instance, **kwargs):
    WorkerModelHistoryModel.objects.create(worker=instance.worker,worker_model=instance.worker_model)
