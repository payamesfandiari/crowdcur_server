import pandas as pd
from sklearn.neighbors import kneighbors_graph
from crowdcur.models import *
from .models import *


def update_similar_workers():
    worker_feats = {}
    worker_ids = sorted(list(User.objects.all().values_list('pk', flat=True)))
    for w in worker_ids:
        worker_feats[w] = _generate_worker_feature(w)
        SimilarWorkersBasedOnModel.objects.create(worker_id=w,similar_workers={})
    features = pd.DataFrame.from_dict(worker_feats,orient='index')

    knn = kneighbors_graph(features,5,include_self=False).tocoo()
    num_workers = len(features)

    for i in range(num_workers):
        worker = SimilarWorkersBasedOnModel.objects.get(pk=worker_ids[i])
        worker.similar_workers['similar'] = []
        inds = knn.getrow(0).indices
        for worker_j in inds:
            worker.similar_workers['similar'].append(worker_ids[worker_j])
        worker.save()


def _generate_worker_feature(worker_id):
    worker = User.objects.get(pk=worker_id)
    keywords = Job.objects.get_keywords()
    mo = worker.workermodel.worker_model
    features = list(TaskFeatureMapping.objects.all().values_list('feature_name'))
    out = {}
    for u in keywords:
        if u in worker.preference:
            out[u] = 1
        else:
            out[u] = 0
    if len(mo) >1:
        for u in mo:
            out[u] = mo[u]
    else:
        for u in features:
            out[u] = 0

    out['age'] = worker.age
    return out



