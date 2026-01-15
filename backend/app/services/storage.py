"""
Object Storage Interface
Unified interface for Local FS, AWS S3, and MinIO.
"""
import os

class StorageDriver:
    def __init__(self, provider="local"):
        self.provider = provider
    
    def upload_file(self, file_path: str, destination: str):
        if self.provider == "local":
            return f"stored_locally:/{destination}"
        elif self.provider == "s3":
            # boto3.client('s3').upload_file(...)
            return f"s3://bucket/{destination}"
            
    def get_url(self, file_key: str):
        if self.provider == "local":
            return f"/static/{file_key}"
        return f"https://s3.amazonaws.com/bucket/{file_key}"

storage = StorageDriver(provider=os.getenv("STORAGE_PROVIDER", "local"))
