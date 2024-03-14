from flask import Flask, request
import pandas as pd
import warnings
import requests
import boto3
from boto3 import Session
import subprocess

# session = Session()
# credentials = session.get_credentials()
# current_creds = credentials.get_frozen_credentials()

sqs = boto3.client('sqs', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

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

    response = sqs.receive_message(
    QueueUrl = req_queue_url,
    VisibilityTimeout=15
    )
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        filename = message['Body']
        print(filename)
        # file_obj = s3.get_object(
        #     Key=filename,
        #     Bucket='1229560048-in-bucket'
        #     )
        file = s3.download_file('1229560048-in-bucket', filename, 'D:/Amogh/Resume/{}'.format(filename))
        prediction = subprocess.check_output("python3 face_recognition.py D:/Amogh/Resume/{}".format(filename), shell=True)
        print(prediction.decode().strip())
        s3.put_object(Key=filename.split('.')[0],
                      Body=prediction,
                      Bucket=output_bucket)
        sqs.send_message(
            QueueUrl=resp_queue_url,
            MessageBody="{}:{}".format(filename, prediction)
        )
        sqs.delete_message(
            QueueUrl=req_queue_url,
            ReceiptHandle=receipt_handle
        )
    else:
        print("Queue is empty")
        break


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