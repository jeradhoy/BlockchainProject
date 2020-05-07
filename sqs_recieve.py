import logging
import boto3
from botocore.exceptions import ClientError
import time
import json
from random import randint
from typing import *

class Sqs:
    def __init__(self, sqs_config, node_id):

        self.sqs_client = boto3.client('sqs', region_name='us-east-2')
        self.sqs_resource = boto3.resource('sqs', region_name='us-east-2')
        self.nodes_sqs_info = sqs_config["nodes"]

        self.node_id = node_id
        self.my_queue_url = self.nodes_sqs_info[self.node_id]["queue_url"]

        self.leader_sqs_info = sqs_config["leader"]
        self.leader_queue_url = self.leader_sqs_info["queue_url"]
        self.leader_queue_name = self.leader_sqs_info["queue_name"]

        self.purge_queues()

    def purge_queues(self):

        try:
            response = self.sqs_client.purge_queue(QueueUrl=self.my_queue_url)
            return response
        except:
            print("purge timeout...")

    def send_message_to_all_other_nodes(self, message):
        message = str(message)

        for node_info in self.nodes_sqs_info:
            if node_info["id"] == self.node_id:
                continue
            print("Sending to node " + str(node_info["id"]) + ": " + message)
            result = self.send_sqs_message(node_info["queue_url"], node_info["queue_name"], message)

    def send_msg_to_node(self, node_id: int, message: str):

        return self.send_sqs_message(self.nodes_sqs_info[node_id]["queue_url"], self.nodes_sqs_info[node_id]["queue_name"], message)

    def send_sqs_message(self, sqs_queue_url, queue_name, msg_body):

        print("Outgoing message: " + msg_body)
        # Send the SQS message
        queue = self.sqs_resource.get_queue_by_name(QueueName=queue_name)
        try:
            dedup_id = str(randint(0,1e10))
            msg = queue.send_message(QueueUrl=sqs_queue_url,
                                        MessageBody=msg_body, MessageGroupId='string', MessageDeduplicationId=dedup_id)

        except ClientError as e:
            print("ERROR yo!")
            print(e)
            logging.error(e)
            return None
        return msg

    def send_to_leader(self, message):

        return self.send_sqs_message(self.leader_queue_url, self.leader_queue_name, message)

    def retrieve_leader_message(self):

        return self.retrieve_sqs_messages(self.leader_queue_url)


    def retrieve_sqs_messages(self, queue_url=None, num_msgs=1, wait_time=0, visibility_time=1):

        # Assign this value before running the program
        num_messages = 1

        if queue_url is None:
            queue_url = self.my_queue_url

        # Retrieve messages from an SQS queue
        try:
            msgs = self.sqs_client.receive_message(QueueUrl=queue_url,
                                            MaxNumberOfMessages=num_msgs,
                                            WaitTimeSeconds=wait_time,
                                            VisibilityTimeout=visibility_time)
            if "Messages" not in msgs:
                return None

            # string message 
            msg = msgs["Messages"][0]

            # Remove the message from the queue
            self.sqs_client.delete_message(QueueUrl=queue_url,
                                    ReceiptHandle=msg['ReceiptHandle'])

            print("Incoming Message: " + msg["Body"])
            return msg["Body"]
            

        except ClientError as e:
            print(e)
            logging.error(e)
            return None
