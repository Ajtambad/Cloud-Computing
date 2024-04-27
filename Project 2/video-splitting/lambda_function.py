#__copyright__   = "Copyright 2024, VISA Lab"
#__license__     = "MIT"

from boto3 import client as boto3_client
import subprocess
import os
import json

stage_1_bucket = '1229560048-stage-1'
input_bucket = '1229560048-input'

s3 = boto3_client('s3', region_name='us-east-1')
lambdaClient = boto3_client('lambda', region_name='us-east-1')

def lambda_handler(event, context):

    video_filename = event['Records'][0]['s3']['object']['key']
    filename = video_filename
    video_filename = os.path.join('/tmp', video_filename)
    file = s3.download_file(input_bucket, filename, video_filename) #Download from input S3 bucket
    outfile = os.path.splitext(filename)[0] + ".jpg"

    if not os.path.exists('/tmp/output'):
        os.makedirs('/tmp/output')

    split_cmd = 'ffmpeg -i ' + video_filename + ' -vframes 1 ' + '/tmp/output/' + outfile
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)

    #Upload to Stage-1 S3 Bucket
    dir = os.listdir('/tmp/output/')
    for file in dir:
        s3.upload_file('/tmp/output/' + file, stage_1_bucket, outfile)

    input = {
        'bucket_name':'1229560048-stage-1',
        'image_file_name': outfile
    }

    response = lambdaClient.invoke(
        FunctionName = 'face-recognition',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(input)
    )

    responsePayload = json.load(response['Payload'])
    print(responsePayload)

    return outfile
