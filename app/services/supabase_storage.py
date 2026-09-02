import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables if not already loaded
load_dotenv()

def get_supabase_client() -> Client:

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in your .env file or environment."
        )

    return create_client(supabase_url, supabase_key)



def upload_excel_to_supabase(excel_buffer, expires_in_seconds: int = 2592000) -> str:
    """
    Uploads in-memory Excel buffer to Supabase Private Bucket 
    and returns a signed download URL valid for 30 days (2,592,000 seconds).
    """
    BUCKET_NAME = "resources"
    supabase = get_supabase_client()

    file_bytes = excel_buffer.getvalue()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destination_path = f"group_exports/Groups_Report_{timestamp}.xlsx"

    # 1. Upload raw bytes to Supabase Storage
    supabase.storage.from_(BUCKET_NAME).upload(
        path=destination_path,
        file=file_bytes,
        file_options={
            "content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "x-upsert": "true"
        }
    )

    # 2. Generate 30-Day Signed URL
    response = supabase.storage.from_(BUCKET_NAME).create_signed_url(
        path=destination_path,
        expires_in=expires_in_seconds
    )

    signed_url = response.get("signedUrl") if isinstance(response, dict) else response["signedUrl"]
    return signed_url