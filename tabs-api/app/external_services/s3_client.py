from io import BytesIO
import boto3
from botocore.config import Config

from app.core.config import settings
from app.exceptions.s3 import S3ClientException
from app.utils.logging import Logger, LogLevel


class S3Client:
    """
    A utility class for interacting with DigitalOcean Spaces (S3-compatible storage).

    Handles uploading, deleting, and generating presigned URLs for files stored in a bucket.
    """
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=settings.digital_ocean_bucket_region_name,
            endpoint_url=f"https://{settings.digital_ocean_bucket_region_name}.digitaloceanspaces.com",
            aws_access_key_id = settings.digital_ocean_bucket_access_key_id,
            aws_secret_access_key = settings.digital_ocean_bucket_secret_key,
            config=Config(s3={'addressing_style': 'virtual'})
        )
        self.bucket_name = settings.digital_ocean_bucket_name

    def generate_presigned_url(self, object_name: str, expires_in: int = 3600) -> str:
        """
        Generate a presigned URL for temporary access to file.
        """
        Logger.log(LogLevel.INFO, f"Generating presigned URL for {object_name}")

        try:
            url = self.s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self.bucket_name, "Key": object_name},
                ExpiresIn=expires_in,
            )
            return url
        except Exception as e:
            Logger.log(LogLevel.ERROR, f"Error generating presigned URL for {object_name}: {e}")
            raise S3ClientException()

    async def upload_fileobj(self, object_name, file) -> None:
        """
        Upload file with name object_name to s3 bucket.
        """
        Logger.log(LogLevel.INFO, f"Uploading {object_name}, file - {file}")
        try:
            file_bytes = await file.read()
            file_obj = BytesIO(file_bytes)

            self.s3.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_name,
                ExtraArgs={
                    "ContentType": "application/pdf",
                    "ContentDisposition": "inline",
                    "CacheControl": "public, max-age=31536000, immutable",
                }
            )
        except Exception as e:
            Logger.log(LogLevel.ERROR, str(e))
            raise S3ClientException()

    def delete_object(self, object_name: str) -> None:
        """
        Delete file with name object_name from s3 bucket.
        """
        Logger.log(LogLevel.INFO, f"Deleting {object_name}")
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)
        except Exception as e:
            Logger.log(LogLevel.ERROR, f"Error deleting object {object_name}: {e}")
            raise S3ClientException()


def get_s3_client() -> S3Client:
    return S3Client()