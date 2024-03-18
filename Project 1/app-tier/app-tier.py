from flask import Flask, request
import pandas as pd
import warnings
import requests
import boto3
from boto3 import Session
import subprocess
import os
import time

# session = Session()
# credentials = session.get_credentials()
# current_creds = credentials.get_frozen_credentials()

sqs = boto3.client('sqs', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
req_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue'
resp_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-resp-queue'
input_bucket = '1229560048-in-bucket'
output_bucket = '1229560048-out-bucket'

warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)


classResDict = {}

classRes = pd.read_csv('../Classification Results.csv')

for ele in classRes.iterrows():
    classResDict[ele[1][0]] = ele[1][1]

while True:

    #Reading filename from REQUESTS SQS QUEUE.
    response = sqs.receive_message(
    QueueUrl = req_queue_url,
    VisibilityTimeout=15,
    MaxNumberOfMessages=3,
    )
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        filename = message['Body']
        file = s3.download_file(input_bucket, filename, filename) #Downloading file from INPUT S3 BUCKET using the filename received from the REQUEST SQS QUEUE.
        pred_output = subprocess.run("python3 face_recognition.py {}".format(filename), shell=True, capture_output=True)
        prediction = pred_output.stdout.decode().strip()

        #Generating predictions with the model and putting it in the S3 OUTPUT BUCKET.
        s3.put_object(Key=filename.split('.')[0],
                      Body=prediction,
                      Bucket=output_bucket)
        
        #Sending the filename and the prediction in the expected format to the RESPONSE QUEUE. 
        print("{}:{}".format(filename.split('.')[0], prediction))
        sqs.send_message(
            QueueUrl=resp_queue_url,
            MessageBody="{}:{}".format(filename.split('.')[0], prediction,)
        )

        #Deleting messages from the REQUEST QUEUE that were received.
        sqs.delete_message(
            QueueUrl=req_queue_url,
            ReceiptHandle=receipt_handle
        )
    else:
        print("Queue is empty")
        time.sleep(3)
        continue


# @app.route("/", methods=["GET", "POST"])
# def file_upload():
#     if request.method=="POST":
#         form = request.files['inputFile']
#         filename = form.filename.split('.')[0]
#         # ans_dict[filename] = classResDict[filename]
#         # return "{}:{}".format(filename, classResDict[filename])
#         # requests.post('http://44.197.210.121:80', data=ans_dict)
#         return "Nothing"
#     else:
#         print(response)
#         return "Server is running"

if __name__ == "__main__":
    app.run(debug=True)