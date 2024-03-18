import boto3
from boto3 import Session
import time

# session = Session()
# credentials = session.get_credentials()
# current_creds = credentials.get_frozen_credentials()
ec2 = boto3.resource('ec2', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

req_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue'
resp_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-resp-queue'

def get_queue_messages():
    queue_att = sqs.get_queue_attributes(QueueUrl=req_queue_url,
                                        AttributeNames=['ApproximateNumberOfMessages','ApproximateNumberOfMessagesNotVisible'])
    return int(queue_att['Attributes']['ApproximateNumberOfMessages']) + int(queue_att['Attributes']['ApproximateNumberOfMessagesNotVisible'])

def num_instances_to_create(num_mess) -> int:
    return min(num_mess, 19)

def create_instances(total_instances):
    count = 0
    for i in range(total_instances):
        
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
        count += 1
    return count

def all_instance_count():
    count = 0
    for instance in ec2.instances.all():
        if (instance.state['Name'] == 'running' or instance.state['Name'] == 'pending') and instance.id != 'i-074ec05ec1e589838':
            count += 1
    return count

def running_instance_list():
    instances=[]
    for instance in ec2.instances.all():
        if (instance.state['Name'] == 'running') and instance.id != 'i-074ec05ec1e589838':
            instances.append(instance)
    return instances

def terminate_instances(num_mess, instances):
    curr_num_mess = num_mess

    #It should enter the loop ONLY if there are more than 0 messages in the queue AND if there are more than 0 instances running.
    while (num_mess > 0 or (curr_num_mess != 1 and curr_num_mess != 0)) and len(instances)>0:
        time.sleep(1)
        print(num_mess)
        curr_num_mess = num_mess
        num_mess = get_queue_messages()

        #It should enter the loop ONLY after messages from REQUEST queue have moved to the RESPONSE queue.
        while (curr_num_mess - num_mess) > 0 and len(instances) > 0:
            #Code to Terminate Instance
            print(instances[0].id)
            resp = instances[0].terminate()
            instances.remove(instances[0])
            curr_num_mess -= 1
        
if __name__ == "__main__":
    
    running_instances = []
    created_instances = []
    targetInstanceNum = 0
    instancesCreated=0

    while True:
        time.sleep(5)
        num_messages_req = get_queue_messages()
        if num_messages_req > 0:
            targetInstanceNum = num_instances_to_create(num_messages_req) #If REQ QUEUE < 19 messages, then targetInstance=num_messages 
                                                                        #Else, targetInstance=19
            instanceCount = all_instance_count() #Number of pending + running instances
                
            while instanceCount < targetInstanceNum: 
                instanceCount = targetInstanceNum - instanceCount
                create_instances(instanceCount) #Create more instances if running + pending is less than 
                                                                         #how many instances we need. 
            instancesCreated = instanceCount

            running_instances = running_instance_list()
            terminate_instances(instancesCreated, running_instances)
            break


        

