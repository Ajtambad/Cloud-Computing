from flask import Flask, request, redirect
import warnings
import boto3
import time

sqs = boto3.resource('sqs', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

req_queue = sqs.get_queue_by_name(QueueName="1229560048-req-queue")
resp_queue = sqs.get_queue_by_name(QueueName="1229560048-resp-queue")
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
        req_queue.send_message(MessageBody=filename)

        while True:
            #Receiving final prediction from the RESPONSE SQS QUEUE. 
            responses = resp_queue.receive_messages(
            VisibilityTimeout=15,
            MaxNumberOfMessages=10
            )
            for resp in reversed(responses):
                if resp:
                    prediction = resp.body
                    print(prediction)

                    #Deleting messages from the RESPONSE SQS QUEUE after receiving predictions succesfully. 
                    if prediction.split(':')[0] == filename.split('.')[0]:
                        resp.delete()
                        return prediction
                else:
                    print("Queue is Empty")
                    continue

        return "Running complete!" 
    else:
        return "Server is running!"


if __name__ == "__main__":
    app.run(debug=False)