
import os
import io
import boto3
import json
import csv


# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime_client= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    #payload = json.dumps(data)
    
    #payload = "\n".join(str(v) for v in payload )
    
    payload_all = ''
    for row in payload:
        str_row = ','.join([str(item) for item in row]) + "\n" 
        payload_all += str_row
    response = runtime_client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME, ContentType='text/csv', Body=payload_all
    )
    result = response["Body"].read()
    result = result.decode("utf-8")
    result = result.strip("\n0").split("\n")
    preds = list(map(float,result))
    return  preds

