import uuid
import numpy as np
from sklearn.cluster import DBSCAN

def cluster_faces(photo_embeddings):
    vectors = np.array([e for _, e in photo_embeddings])
    photo_ids = [pid for pid, _ in photo_embeddings]

    clustering = DBSCAN(eps=0.6, min_samples=2).fit(vectors)

    clusters = {}
    for label, pid in zip(clustering.labels_, photo_ids):
        if label == -1:
            continue
        clusters.setdefault(label, []).append(pid)

    return {str(uuid.uuid4()): v for v in clusters.values()}
