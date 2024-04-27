from boto3 import client as boto3_client
import subprocess
import os

s3 = boto3_client('s3', region_name='us-east-1')

output_bucket = '1229560048-output'
package_bucket = '1229560048-package'

def handler(event, context):
# def handler():

    stage_1_bucket = event['bucket_name']
    filename = event['image_file_name']
    # stage_1_bucket = '1229560048-stage-1'
    # filename = 'test_4.jpg'
    file_path = os.path.join('/tmp', filename)

    file = s3.download_file(stage_1_bucket, filename, file_path)
    s3.download_file(package_bucket, 'data.pt', '/tmp/data.pt')
    s3.download_file(package_bucket, 'face-recognition-code.py', '/tmp/face-recognition-code.py')
    
    print("Before running the face recognition")
    pred_output = subprocess.run("python3 /tmp/face-recognition-code.py {}".format(file_path), shell=True, capture_output=True)
    prediction = pred_output.stdout.decode().strip()
    print("After running the face recognition")
    
    file_upload = s3.put_object(Key=filename.split('.')[0] + '.txt',
                      Body=prediction,
                      Bucket=output_bucket)
    
    print(file_upload)
    return "Something"
    # extraction_folder_name = output.stdout.decode().strip()

    # s3.upload_file(extraction_folder_name, output_bucket, filename)

if __name__ == "__main__":
    handler()
