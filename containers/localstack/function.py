import json
import os
import zipfile
from io import BytesIO
from pprint import pprint
from urllib import error, request

import boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=os.environ["LAMBDA_TOKEN"],
    endpoint_url=os.environ["AWS_S3_ENDPOINT_URL"],
    region_name=os.environ["AWS_DEFAULT_REGION"],
)


def register_csv(id, csv_name):
    lambda_token = os.environ["LAMBDA_TOKEN"]

    url = f"http://app:8000/api/register_customer/"
    data = {"token": lambda_token, "id": id, "csv_name": csv_name}
    headers = {
        "Content-Type": "application/json",
    }
    get_req = request.Request(url, json.dumps(data).encode(), headers)
    try:
        with request.urlopen(get_req) as res:
            body = json.loads(res.read())
            headers = res.getheaders()
            status = res.getcode()
            pprint(headers)
            pprint(status)
            pprint(body)
    except error.HTTPError as e:
        pprint(e)

    return True


def lambda_handler(event, context):
    print("lambda_handler")
    bucket = os.environ["AWS_STORAGE_BUCKET_NAME"]
    body = json.loads(event["Records"][0]["body"])
    print(f"body:{body}")
    zip_name = body["file"]

    try:
        obj = s3.get_object(Bucket=bucket, Key=zip_name)
        z = zipfile.ZipFile(BytesIO(obj["Body"].read()))
    except Exception as e:
        print(str(e))
    finally:
        s3.delete_object(Bucket=bucket, Key=zip_name)
        return {}
