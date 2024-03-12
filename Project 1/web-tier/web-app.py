from flask import Flask, request, redirect
import pandas as pd
import warnings
import requests
import boto3
from botocore.config import Config

sqs = boto3.client('sqs')

req_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue'
resp_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-resp-queue'

warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method == "POST":
        form = request.files['inputFile']
        filename = form.filename
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
                receipt_handle=resp['ReceiptHandle']
                print(message)
                sqs.delete_message(
                    QueueUrl=resp_queue_url,
                    ReceiptHandle=receipt_handle
                )
            else:
                print("Queue is empty")  

    else:
        return "Server is running!"
    
if __name__ == "__main__":
    app.run(debug=False)