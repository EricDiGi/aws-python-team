import json
import os

def lambda_handler(event, context):
    print(event)
    print(context)
    print(os.environ)
    return {
        "statusCode": 200,
        "body": json.dumps("Hello from Lambda!"),
    }
