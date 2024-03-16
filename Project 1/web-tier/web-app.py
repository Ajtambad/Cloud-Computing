from flask import Flask, request, redirect
import pandas as pd
import warnings
import requests
import boto3
from botocore.config import Config
import os

sqs = boto3.client('sqs', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

req_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue'
resp_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-resp-queue'
input_bucket = '1229560048-in-bucket'

warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def file_upload():

    #Listening for POST requests.
    if request.method == "POST":
        form = request.files.get('inputFile')
        filename = form.filename
        file_content = form.read()

        #Putting the filename and the file itself into the INPUT S3 BUCKET.
        s3.put_object(
            Key=filename,
            Body=file_content,
            Bucket=input_bucket
        )

        #Sending the filename to the REQUEST SQS QUEUE. 
        response = sqs.send_message(
            QueueUrl = req_queue_url,
            MessageBody=filename
        )
        while True:

            #Receiving final prediction from the RESPONSE SQS QUEUE. 
            resp = sqs.receive_message(
            QueueUrl=resp_queue_url,
            VisibilityTimeout=0,
            WaitTimeSeconds=5,
            )
            if 'Messages' in resp:
                message = resp['Messages'][0]
                receipt_handle=message['ReceiptHandle']
                prediction = message['Body']
                print(prediction)

                #Deleting messages from the RESPONSE SQS QUEUE after receiving predictions succesfully. 
                sqs.delete_message(
                    QueueUrl=resp_queue_url,
                    ReceiptHandle=receipt_handle
                    )
            else:
                break
        return "Running complete!" 
    else:
        return "Server is running!"


if __name__ == "__main__":
    app.run(debug=False)