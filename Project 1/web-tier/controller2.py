import time

import boto3

req_queue_url = "https://sqs.us-east-1.amazonaws.com/211125745270/1229560048-req-queue"

class AutoController:

    def __init__(self, req_queue_url):
        self.sqs = boto3.client('sqs', region_name='us-east-1')
        self.ec2 = boto3.client('ec2', region_name='us-east-1')
        self.req_queue_url = req_queue_url
        self.desiredCapacity = 0
        self.targetToReach = 0
        self.target_not_reached = 0
        self.recAttempts = 15
        self.maxAttempts = 25
        self.instances = [None]*20
        self.runningInstances = [False]*20


    def get_queueLength(self):
        response = self.sqs.get_queue_attributes(
            QueueUrl=self.req_queue_url,
            AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible']
        )
        return int(response['Attributes']['ApproximateNumberOfMessages']) + int(response['Attributes']['ApproximateNumberOfMessagesNotVisible'])


    def running_instances(self):
        count = 0
        instance_ids = [instance_id for instance_id in self.instances if instance_id is not None]
        if len(instance_ids) > 0:
            resp = self.ec2.describe_instance_status(
                InstanceIds=instance_ids,
                IncludeAllInstances=True,
            )
            for instance_status in resp['InstanceStatuses']:
                i = self.instances.index(instance_status['InstanceId'])
                self.runningInstances[i] = instance_status['InstanceState']['Name'] == 'running'
                count = count + (1 if self.runningInstances[i] else 0)
        return count


    def setCapacity(self, capacity):
        self.desiredCapacity = capacity


    def spin_instance(self, name):
        resp = self.ec2.run_instances(
            LaunchTemplate={
                'LaunchTemplateId':'lt-011262481f4b71e5a'
            },
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name,
                        },
                    ]
                },
            ],
            MaxCount=1,
            MinCount=1,
        )
        return resp['Instances'][0]['InstanceId']

    def updateInstanceState(self):
        for i, instance in enumerate(self.instances):
            if i < self.desiredCapacity and instance is not None and not self.runningInstances[i] and self.target_not_reached == self.recAttempts:
                print("Recreating instance: ", i + 1)
                self.ec2.terminate_instances(InstanceIds=[instance])
                self.instances[i] = self.instances[i] = self.spin_instance('app-tier-instance-' + str(i + 1))
            elif i < self.desiredCapacity and instance is None:
                self.instances[i] = self.spin_instance('app-tier-instance-' + str(i + 1))
            elif i >= self.desiredCapacity and instance is not None:
                 self.ec2.terminate_instances(InstanceIds=[instance])
                 self.instances[i] = None

    def scaleDownFlag(self, current_instance_count):
        if current_instance_count < self.targetToReach:
            self.target_not_reached += 1
            if self.target_not_reached == self.maxAttempts:
                print("Max Attempts Reached. Scaling down")
                self.target_not_reached = 0
                self.targetToReach = 0
                return True
            else:
                print("Target: ", self.targetToReach, " not yet reached, not scaling down")
                return False
        print("Target: ", self.targetToReach, " reached, scaling down")
        self.target_not_reached = 0
        self.targetToReach = 0
        return True

    def scale(self):
        instanceCount = self.running_instances()
        queueLen = self.get_queueLength()

        print("Instances: ", instanceCount)
        print("Queue length: ", queueLen)

        if instanceCount < queueLen:
            newInstCount = instanceCount + (queueLen - instanceCount)
            newInstCount = min(20, newInstCount)
            self.targetToReach = max(self.targetToReach, newInstCount)
            print("Setting capacity to: ", self.targetToReach)
            self.setCapacity(self.targetToReach)

        elif instanceCount > queueLen:
            # Do not scale down until targetToReach has been reached.
            if not self.scaleDownFlag(instanceCount):
                self.updateInstanceState()
                return
            newInstCount = instanceCount - (instanceCount - queueLen)
            newInstCount = max(0, newInstCount)
            print("Setting capacity to: ", newInstCount)
            self.setCapacity(newInstCount)

        self.updateInstanceState()


if __name__ == "__main__":
    while True:
        try:
            client = boto3.client('ec2', region_name='us-east-1')
            delInstances = list(
                boto3.resource('ec2', region_name='us-east-1').instances.filter(
                    Filters=[
                        {
                            'Name': 'tag:Name',
                            'Values': ["app-tier-instance*"]
                        },
                    ],
                )
            )
            delInstances = [instance.id for instance in delInstances]
            if len(delInstances) > 0:
                client.terminate_instances(InstanceIds=delInstances)
            auto_controller = AutoController(req_queue_url)
            while True:
                time.sleep(5)
                auto_controller.scale()
        except Exception:
            print("Auto controller not working as expected, trying again")