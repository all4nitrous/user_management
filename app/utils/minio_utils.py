import boto3
from botocore.exceptions import NoCredentialsError

# MinIO Configuration
MINIO_URL = "http://minio:9000"  # MinIO container URL
MINIO_ROOT_USER = "admin"        # Root username from docker-compose.yml
MINIO_ROOT_PASSWORD = "password" # Root password from docker-compose.yml
BUCKET_NAME = "qr-codes"         # Bucket name for storage

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ROOT_USER,
    aws_secret_access_key=MINIO_ROOT_PASSWORD,
)

def upload_file_to_minio(file_path: str, object_name: str):
    """
    Upload a file to the MinIO bucket.
    :param file_path: Path to the file on the local filesystem.
    :param object_name: Name to store the file as in the bucket.
    """
    try:
        s3_client.upload_file(file_path, BUCKET_NAME, object_name)
        print(f"File '{file_path}' uploaded to '{BUCKET_NAME}' as '{object_name}'.")
    except NoCredentialsError:
        print("Error: Missing credentials for MinIO.")
