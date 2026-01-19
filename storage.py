from supabase_client import supabase

BUCKET = "moment-photos"

def get_signed_url(path: str, expires: int = 300):
    res = supabase.storage.from_(BUCKET).create_signed_url(
        path, expires
    )
    return res["signedURL"]
