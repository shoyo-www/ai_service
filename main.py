from fastapi import FastAPI
from pydantic import BaseModel

from supabase_client import supabase
from storage import get_signed_url
from face import get_embedding_from_url
from cluster import cluster_faces

app = FastAPI()


class ProcessMomentRequest(BaseModel):
    moment_id: str


@app.post("/process-moment")
def process_moment(req: ProcessMomentRequest):
    moment_id = req.moment_id

    photos = supabase.table("photos") \
        .select("id, storage_path") \
        .eq("moment_id", moment_id) \
        .execute().data

    if not photos:
        return {"status": "no_photos"}

    embeddings = []

    for photo in photos:
        signed_url = get_signed_url(photo["storage_path"])
        emb = get_embedding_from_url(signed_url)
        if emb:
            embeddings.append((photo["id"], emb))

    if not embeddings:
        return {"status": "no_faces_found"}

    clusters = cluster_faces(embeddings)

    for cluster_id, photo_ids in clusters.items():
        for pid in photo_ids:
            supabase.table("face_clusters").insert({
                "moment_id": moment_id,
                "cluster_id": cluster_id,
                "photo_id": pid,
            }).execute()

    return {
        "status": "ok",
        "cluster_count": len(clusters)
    }
