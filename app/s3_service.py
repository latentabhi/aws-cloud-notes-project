import os
import boto3


def upload_attachment(file_storage, filename):
    bucket = os.getenv("S3_BUCKET", "").strip()
    region = os.getenv("AWS_REGION", "ap-south-1").strip()

    if not bucket:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        upload_dir = os.path.join(base_dir, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        file_storage.save(file_path)
        return f"/uploads/{filename}"

    s3 = boto3.client("s3", region_name=region)
    s3.upload_fileobj(file_storage, bucket, filename)
    return f"https://{bucket}.s3.{region}.amazonaws.com/{filename}"
