import boto3
from boto3 import Session

session = Session()
credentials = session.get_credentials()
current_creds = credentials.get_frozen_credentials()

ec2 = boto3.resource('ec2', region_name='us-east-1', aws_access_key_id=current_creds.access_key, aws_secret_access_key=current_creds.secret_key)

ami_id = "ami-00ddb0e5626798373"
instance = ec2.create_instances(
           ImageId=ami_id,
           MinCount=1,
           MaxCount=1,
           InstanceType="t2.micro",
           TagSpecifications=[{'ResourceType':'instance',
                               'Tags': [{
                               'Key': 'Name',
                               'Value': 'app-tier-instance'}]}])

ec2.create_tags(Resources=['ami-00ddb0e5626798373'], Tags=[{'Key':'Name', 'Value':'app-tier-instance'}])

# instance = ec2.run_instances(
#            ImageId=ami_id,
#            MinCount=1,
#            MaxCount=1,
#            InstanceType="t2.micro",
#            TagSpecifications=[{'ResourceType': 'instance',
#                                'Tags': [{
#                                 'Key': 'Name',
#                                 'Value': 'WebTier Worker' }]}])