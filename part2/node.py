import random
import time
import sys
import json

from block import Block
from blockchain import Blockchain
sys.path.append("../")
from sqs_recieve import Sqs
from transaction import Transaction


class Node:
    def __init__(self, nodeId, amoutAtStake, sqs_instance):

        self.nodeId = nodeId
        self.amoutAtStake = amoutAtStake
        self.sqs_instance = sqs_instance

        self.accruedRewards = 0
    


        # means that they can create the block
        self.isCreator = False

        self.bc = Blockchain("verifier_" + str(id) + ".txt")

        # put dummie values in this for now for testing
        self.totalAtStakeDict = {0: 1000, 1: 2000, 3: 3000, 4: 500}
        # self.atStakeDict = {}
        # self.atStakeDict[nodeId] = amoutAtStake

        self.stakeArray = []

        # means that they can select who creates the block
        self.isLeader = False

        self.leader_timeout_time = time.time() + 5
        self.in_election_timeout_time = 0
        self.holdingElection = False


    # when we recieve amount at stake from leader queue we append them
    # by node id to index
    def appendToTotalAtStake(self, amount, nodeId):
        if self.isLeader:
            self.amoutAtStake[self.nodeId] = self.amoutAtStake
            self.totalAtStakeDict[nodeId] = amount

    def generateStakeArray(self):
        s = {k: v for k, v in sorted(self.totalAtStakeDict.items(), key=lambda item: item[1], reverse=True)}
        self.totalAtStakeDict = s
        number = len(self.totalAtStakeDict)
        for node in self.totalAtStakeDict:
            for i in range(number):
                self.stakeArray.append(node)
            number -= 1

    def commitBlockToBlockchain(self, block: Block):

        success = self.bc.addBlockToChain(block)
        self.accruedRewards += block.getRewards(self.nodeId)

        

    def pickCreator(self):
        #   select which node can create block based on stake and send alert this node of that    
        self.generateStakeArray()
        waitTime = random.randint(5, 15)
        time.sleep(waitTime)
        creatorNode = random.choice(self.stakeArray)
        return creatorNode

    def start_election(self):

        election_msg = json.dumps({"type": "BullyElection", "nodeId": self.nodeId})

        for node_sqs in self.sqs_instance.nodes_sqs_info:
            if node_sqs["id"] > self.nodeId:
                self.sqs_instance.send_msg_to_node(node_sqs["id"], election_msg)

        self.holdingElection = True
        self.isLeader = False
        self.leader_timeout_time = time.time() + 30
        self.in_election_timeout_time = time.time() + 10

            
    def send_bully_leader(self):
        msg = json.dumps({"type": "BullyLeader"})
        for node_sqs in self.sqs_instance.nodes_sqs_info:
            if node_sqs["id"] < self.nodeId:
                self.sqs_instance.send_msg_to_node(node_sqs["id"], msg)

    def receive_loop(self):

        bully_leader_msg_timeout = 0

        while True:

            if self.holdingElection == True:
                if time.time() > self.in_election_timeout_time:
                    print("Won Election, I'm the Leader!")
                    self.isLeader = True
                    self.holdingElection = False
                    self.send_bully_leader()
                    bully_leader_msg_timeout = time.time() + 5

            if self.isLeader == True:
                if time.time() > bully_leader_msg_timeout:
                    self.send_bully_leader()
                    bully_leader_msg_timeout = time.time() + 5
            
            # Check if leader has timedout
            if time.time() > self.leader_timeout_time:
                print("Timeout!")
                self.start_election()

            msg = self.sqs_instance.retrieve_sqs_messages()

            if msg == None:
                continue

            # print(msg)
            msg_json = json.loads(msg)
            print(msg_json)

            if msg_json["type"] == "BullyElection":
                if msg_json["nodeId"] < self.nodeId:
                    ok_msg = json.dumps({"type": "BullyOK", "nodeId": self.nodeId})
                    self.sqs_instance.send_msg_to_node(msg_json["nodeId"], ok_msg)
                    self.start_election()

            if msg_json["type"] == "BullyOK":
                print("Received OK, standing down!")
                self.holdingElection = False
                # self.isLeader = False

            if msg_json["type"] == "BullyLeader":
                self.leader_timeout_time = time.time() + 30






        
    def mainloop(self):

        while True:

            print("")
            print("Please select from the following menu:")
            print("1. Add money to account.") 
            print("2. Send money someone.") 
            print("3. Print blockchain") 

            print("")

            user_input = input()

            if user_input == "1":

                account = input("Enter the account name: ")
                amount = float(input("Enter the amount to add: "))

                trans = Transaction()
                trans.add_coinbase(account, amount)

            elif user_input == "2":

                from_act = input("Enter the account to send money *from*: ")
                to_act = input("Enter the account to send money *to*: ")
                amt = float(input("Enter the amount to transfer: "))

                trans = Transaction()
                trans.add_transfer(from_act, to_act, amt)

            elif user_input == "3":
                self.bc.print()
                continue

            else:
                continue

            # Send transaction to other nodes
            msg = json.dumps({"Transaction": trans.to_json()})
            self.sqs_instance.send_message_to_all_other_nodes(msg)

            self.bc.transaction_queue.append(trans)
        







    
