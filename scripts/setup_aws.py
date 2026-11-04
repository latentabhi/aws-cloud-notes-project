import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

bucket = os.getenv("S3_BUCKET", "").strip()
region = os.getenv("AWS_REGION", "ap-south-1").strip()


def setup():
    if not bucket:
        print("S3_BUCKET is not set in your .env file.")
        return

    print(f"Creating S3 bucket '{bucket}' in {region}...")
    s3 = boto3.client("s3", region_name=region)

    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print("Bucket created successfully.")
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            print("Bucket already exists.")
        else:
            print(f"Failed to create bucket: {e}")


if __name__ == "__main__":
    setup()
