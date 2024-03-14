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

prediction='Something'
@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method == "POST":
        form = request.files.get('inputFile')
        filename = form.filename
        file_content = form.read()
        s3.put_object(
            Key=filename,
            Body=file_content,
            Bucket=input_bucket
        )
        response = sqs.send_message(
            QueueUrl = req_queue_url,
            MessageBody=filename
        )
        while True:
            resp = sqs.receive_message(
            QueueUrl=resp_queue_url,
            VisibilityTimeout=15
            )
            if 'Messages' in resp:
                message = resp['Messages'][0]
                receipt_handle=message['ReceiptHandle']
                prediction = message['Body']
                sqs.delete_message(
                    QueueUrl=resp_queue_url,
                    ReceiptHandle=receipt_handle
                    )
            else:
                break
        return prediction 
    else:
        return "Server is running!"

              
if __name__ == "__main__":
    app.run(debug=False)