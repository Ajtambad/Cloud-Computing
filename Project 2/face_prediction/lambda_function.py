from boto3 import client as boto3_client
import subprocess
import os

s3 = boto3_client('s3', region_name='us-east-1')

output_bucket = '1229560048-output'

def lambda_handler(event, context):
# def lambda_handler():

    stage_1_bucket = event['bucket_name']
    filename = event['image_file_name']
    # stage_1_bucket = '1229560048-stage-1'
    # filename = 'test_4.jpg'
    file_path = os.path.join('/tmp', filename)

    file = s3.download_file(stage_1_bucket, filename, file_path)
    
    output = subprocess.run("python3 face-extraction-code.py {}".format(file_path), shell=True, capture_output=True)
    print(output)
    return "Something"
    # extraction_folder_name = output.stdout.decode().strip()

    # s3.upload_file(extraction_folder_name, output_bucket, filename)

# if __name__ == "__main__":
#     lambda_handler()
