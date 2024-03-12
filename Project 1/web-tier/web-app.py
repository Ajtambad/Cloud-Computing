from flask import Flask, request, redirect
import pandas as pd
import warnings
import requests
import boto3
from botocore.config import Config

my_config = Config(
    region_name = 'us_east_1'
)

sqs = boto3.client('sqs', config=my_config)

queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue'


warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)

# classResDict = {}

# classRes = pd.read_csv('Classification Results.csv')

# for ele in classRes.iterrows():
#     classResDict[ele[1][0]] = ele[1][1]


@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method == "POST":
        form = request.files['inputFile']
        filename = form.filename
        response = sqs.send_message(
            QueueUrl = queue_url,
            MessageBody=filename
        )
        # redirect('https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue', code=307)
        # return "{}:{}".format(filename, ans_dict[filename])
        return response
    else:
        return "Server is running!"
    
if __name__ == "__main__":
    app.run(debug=False)