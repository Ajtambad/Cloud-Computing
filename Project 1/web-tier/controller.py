import boto3
from boto3 import Session
import time

session = Session()
# credentials = session.get_credentials()
# current_creds = credentials.get_frozen_credentials()

ec2 = boto3.resource('ec2', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

req_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue'
resp_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-resp-queue'

queue_att = sqs.get_queue_attributes(QueueUrl=req_queue_url,
                                     AttributeNames=['ApproximateNumberOfMessages','ApproximateNumberOfMessagesDelayed'])
num_messages_req = int(queue_att['Attributes']['ApproximateNumberOfMessages'])

for i in range(min(num_messages_req, 18)):

    ami_id = "ami-0440d3b780d96b29d"
    instance = ec2.create_instances(
        LaunchTemplate={'LaunchTemplateId':'lt-011262481f4b71e5a'},
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{'ResourceType':'instance',
                            'Tags': [{
                                'Key': 'Name',
                                'Value': 'app-tier-instance-{}'.format(i+1)}]
                                }],
    )

instances = []
for instance in ec2.instances.all():
    if (instance.state['Name'] == 'running' or instance.state['Name'] == 'pending') and instance.id != 'i-0cb090d3c3103a7a4':
        instances.append(instance)

# curr_num_mess = num_messages_req
# while num_messages_req > 0 or (curr_num_mess != 1 and curr_num_mess != 0):
#     while len(instances) > 0:
#         time.sleep(1)
#         print(num_messages_req)
#         curr_num_mess = num_messages_req
#         attributes = sqs.get_queue_attributes(QueueUrl=req_queue_url,
#                                             AttributeNames=['ApproximateNumberOfMessages','ApproximateNumberOfMessagesDelayed'])
#         num_messages_req = int(attributes['Attributes']['ApproximateNumberOfMessages'])
#         while (curr_num_mess - num_messages_req) > 0:
#             #Code to Terminate Instance
#             print(instances[0].id)
#             resp = instances[0].terminate()
#             instances.remove(instances[0])
#             curr_num_mess -= 1