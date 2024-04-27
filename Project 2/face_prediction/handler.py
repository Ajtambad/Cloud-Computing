from boto3 import client as boto3_client
import subprocess
import os
import torch

s3 = boto3_client('s3', region_name='us-east-1')

output_bucket = '1229560048-output'
package_bucket = '1229560048-package'

print("Outside function")

def handler(event, context):
# def handler():
    print("your mom")
    stage_1_bucket = event['bucket_name']
    filename = event['image_file_name']
    # stage_1_bucket = '1229560048-stage-1'
    # filename = 'test_4.jpg'
    file_path = os.path.join('/tmp/', filename)
    print(file_path)
    file = s3.download_file(stage_1_bucket, filename, file_path)
    s3.download_file(package_bucket, 'data.pt', '/tmp/data.pt')
    ls_op = subprocess.run('ls', shell=True, capture_output=True)
    print(ls_op)
    pred_output = subprocess.run("python3 face-recognition-code.py {}".format(file_path), shell=True, capture_output=True)
    print(pred_output)
    prediction = pred_output.stdout.decode().strip()
    print(prediction)
    file_upload = s3.put_object(Key=filename.split('.')[0] + '.txt',
                      Body=prediction,
                      Bucket=output_bucket)
    
    return "Something"
    # extraction_folder_name = output.stdout.decode().strip()

    # s3.upload_file(extraction_folder_name, output_bucket, filename)
