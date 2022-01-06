import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import json
import os

import requests

BUCKET = os.environ['BUCKET']
INPREFIX = os.environ['INPREFIX']

s3_client = boto3.client(
    's3'
)


def lambda_handler(event, context):
    body = json.loads(event['body'])
    r = s3_client.generate_presigned_post( Bucket = BUCKET, Key = INPREFIX + "/" + body['file_name'], ExpiresIn=20)

    return {
        'body':json.dumps(r),
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }


