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

        self.purge_queues()

        # self.leader_sqs_info = sqs_config["leader"]
        # self.clients_sqs_info = sqs_config["clients"]

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
            #print(result)

    def send_sqs_message(self, sqs_queue_url, queue_name, msg_body):

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


    def retrieve_sqs_messages(self, num_msgs=1, wait_time=0, visibility_time=1):

        # Assign this value before running the program
        num_messages = 1

        # Retrieve messages from an SQS queue
        try:
            msgs = self.sqs_client.receive_message(QueueUrl=self.my_queue_url,
                                            MaxNumberOfMessages=num_msgs,
                                            WaitTimeSeconds=wait_time,
                                            VisibilityTimeout=visibility_time)
            if "Messages" not in msgs:
                return None

            # string message 
            msg = msgs["Messages"][0]

            # Remove the message from the queue
            self.sqs_client.delete_message(QueueUrl=self.my_queue_url,
                                    ReceiptHandle=msg['ReceiptHandle'])
            return msg["Body"]
            

        except ClientError as e:
            print(e)
            logging.error(e)
            return None


# def initListener(sqs_queue_url, dist_dict, CONFIG):

#     # Assign this value before running the program
#     num_messages = 1
#     sqs_client = boto3.client('sqs')

#     while True:
#         # time.sleep(2)
#         # Retrieve SQS messages
#         msgs = retrieve_sqs_messages(sqs_queue_url, sqs_client, num_messages)
#         if msgs is not None:
#             for msg in msgs:

#                 msg_json = json.loads(msg["Body"])

#                 dist_dict.receive(msg_json)

#                 # Remove the message from the queue
#                 delete_sqs_message(sqs_queue_url, msg['ReceiptHandle'])
#                 conflict_occured = dist_dict.fix_meeting_conflicts()

#                 if conflict_occured:
#                     # print("Conflict on receive, updating!")
#                     for node in CONFIG["nodes"]:
#                         if node["id"] != dist_dict.node_id:
#                             message = dist_dict.send(node["id"])
#                             send_sqs_message(node["queue_url"], node["queue_name"], json.dumps(message))


# def send_sqs_message(sqs_resource, sqs_queue_url, queue_name, msg_body):

#     # Send the SQS message
#     queue = sqs_resource.get_queue_by_name(QueueName=queue_name)
#     try:
#         dedup_id = str(randint(0,1e10))
#         msg = queue.send_message(QueueUrl=sqs_queue_url,
#                                       MessageBody=msg_body, MessageGroupId='string', MessageDeduplicationId=dedup_id)

#     except ClientError as e:
#         print("ERROR yo!")
#         print(e)
#         logging.error(e)
#         return None
#     return msg
