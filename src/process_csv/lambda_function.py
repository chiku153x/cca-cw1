import boto3
import json


def lambda_handler(event, context):

    return {
        'body':json.dumps({"aaaa":"bbb"}),
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }


