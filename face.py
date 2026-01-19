import cv2
import numpy as np
import requests
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0)

def get_embedding_from_url(url: str):
    r = requests.get(url, timeout=10)
    img = cv2.imdecode(np.frombuffer(r.content, np.uint8), 1)
    faces = app.get(img)
    if not faces:
        return None
    return faces[0].embedding.tolist()
