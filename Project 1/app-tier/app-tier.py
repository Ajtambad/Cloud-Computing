from flask import Flask, request
import pandas as pd
import warnings
import requests
import boto3

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue'

warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)


# classResDict = {}

# classRes = pd.read_csv('Classification Results.csv')

# for ele in classRes.iterrows():
#     classResDict[ele[1][0]] = ele[1][1]

response = sqs.receive_message(
    QueueUrl = queue_url,
)

message = response['Messages'][0]
receipt_handle = message['ReceiptHandle']

@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method=="POST":
        form = request.files['inputFile']
        filename = form.filename.split('.')[0]
        # ans_dict[filename] = classResDict[filename]
        # return "{}:{}".format(filename, classResDict[filename])
        # requests.post('http://44.197.210.121:80', data=ans_dict)
        return "Nothing"
    else:
        print(response)
        return "Server is running"

sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)

if __name__ == "__main__":
    app.run(debug=True)