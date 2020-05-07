import random
import time
import sys
import json

from block import Block
from blockchain import Blockchain
sys.path.append("../")
from sqs_recieve import Sqs
from transaction import Transaction
from itertools import chain


class Node:
    def __init__(self, nodeId, amoutAtStake, sqs_instance):

        self.nodeId = nodeId
        self.amoutAtStake = amoutAtStake
        self.sqs_instance = sqs_instance

        self.accruedRewards = 0

        self.bc = Blockchain("verifier_" + str(nodeId) + ".txt")

        # means that they can select who commits the block
        self.isLeader = False

        self.leader_timeout_time = time.time() + 5
        self.in_election_timeout_time = 0
        self.holdingElection = False

        self.p = .8

        self.latest_block: Block = None



    def commitBlockToBlockchain(self, block: Block):

        success = self.bc.addBlockToChain(block)
        if success:
            self.accruedRewards += block.get_rewards(self.nodeId)

            return True
        else:
            return False

        


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
        msg = json.dumps({"type": "BullyLeader", "nodeId": self.nodeId})
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
            if time.time() > self.leader_timeout_time and self.isLeader == False:
                print("Timeout!")
                self.start_election()

            msg = self.sqs_instance.retrieve_sqs_messages()

            if msg == None:
                continue

            # print(msg)
            msg_json = json.loads(msg)
            # print(msg_json)

            if msg_json["type"] == "BullyElection":
                if msg_json["nodeId"] < self.nodeId:
                    ok_msg = json.dumps({"type": "BullyOK", "nodeId": self.nodeId})
                    self.sqs_instance.send_msg_to_node(msg_json["nodeId"], ok_msg)
                    self.start_election()

            if msg_json["type"] == "BullyOK":
                print("Received OK, standing down!")
                self.holdingElection = False

            if msg_json["type"] == "BullyLeader":
                self.isLeader = False
                self.leader_timeout_time = time.time() + 30

            if msg_json["type"] == "Transaction":
                new_trans = Transaction.from_json(msg_json["data"])
                self.bc.transaction_queue.append(new_trans)

            if msg_json["type"] == "ChosenOne":
                # Send block around for signatures
                block_msg = json.dumps({"type": "SignatureRequest", "block": self.latest_block.to_json(), "nodeId": self.nodeId})
                self.sqs_instance.send_message_to_all_other_nodes(block_msg)

            if msg_json["type"] == "SignatureRequest":

                block_to_verify = Block.from_json(msg_json["block"])
                if self.bc.verifyBlock(block_to_verify) == True:
                    print("Verfied request")
                    verify_msg = json.dumps({"type": "SignatureGranted", "block_hash": block_to_verify.hash, "stake": self.amoutAtStake, "nodeId": self.nodeId})
                    self.sqs_instance.send_msg_to_node(msg_json["nodeId"], verify_msg)
                else:
                    print("Did not verfy request")


            if msg_json["type"] == "SignatureGranted":

                if self.latest_block == None:
                    continue

                if msg_json["block_hash"] == self.latest_block.hash:
                    self.latest_block.add_verifier(msg_json["nodeId"])
                    self.latest_block.totalStaked += msg_json["stake"]

                else:
                    print("Hash from signature doesn't match...")

                if self.latest_block.totalStaked >= self.latest_block.get_transaction_total():

                    print("Commmitting my block!")
                    success = self.commitBlockToBlockchain(self.latest_block)
                    if not success:
                        print("Woooaaahhh, why didn't it commit!?")

                    commit_msg = json.dumps({"type": "CommitBlock", "block": self.latest_block.to_json()})
                    self.sqs_instance.send_message_to_all_other_nodes(commit_msg)
                    self.latest_block = None

            if msg_json["type"] == "CommitBlock":

                block_to_commit = Block.from_json(msg_json["block"])
                success = self.commitBlockToBlockchain(block_to_commit)
                if success:
                    print("Committed block to chain!")
                else:
                    print("Did not commit block :( :(")
            
            if msg_json["type"] == "RemoveTransaction":
                print("Removed transaction " + str(msg_json["trans_id"]))
                self.bc.remove_transaction(msg_json["trans_id"])

    def generate_block(self):

        # Generate block from last five transactions
        gen_block = Block(self.bc.getLength(), self.bc.transaction_queue[0:5], self.bc.getPrevHash(), self.nodeId)
        gen_block.totalStaked += self.amoutAtStake
        return gen_block


    # Everybody creates a block with probability p every 20 seconds
    def create_block_loop(self):

        while True:

            if round(time.time()) % 30 != 0:
                continue

            if random.random() < self.p:

                if len(self.bc.transaction_queue) == 0:
                    print("No transactions in queue, no block to create!")
                    time.sleep(1)
                    continue

                print("Creating block!")
                # Create block
                self.latest_block = self.generate_block()

                msg = json.dumps({"type": "BlockGenerated", "block_index": self.latest_block.index, "nodeId": self.nodeId, "stake": self.amoutAtStake})
                self.sqs_instance.send_to_leader(msg)

            else:
                self.latest_block = None
            
            time.sleep(1)




    def leader_loop(self):

        gen_block_timeout_time = 0
        block_index = 0
        node_gen_stakes = {}
        selection_in_process = False

        while True:

            if not self.isLeader:
                continue

            # Assign block
            if time.time() > gen_block_timeout_time and selection_in_process == True:

                select_list = list(chain.from_iterable([k]*v for k,v in node_gen_stakes.items()))
                chosen_node = random.choice(select_list)

                selection_msg = json.dumps({"type": "ChosenOne", "block_index": block_index})
                self.sqs_instance.send_msg_to_node(chosen_node, selection_msg)

                print("Selected node " + str(chosen_node) + " to commit block.")

                node_gen_stakes = {}
                selection_in_process = False
        
            msg = self.sqs_instance.retrieve_leader_message()

            if msg is None:
                continue

            msg_json = json.loads(msg)
            # print(msg_json)

            if msg_json["type"] == "BlockGenerated":

                if time.time() > gen_block_timeout_time:
                    print("Starting node selection!")
                    gen_block_timeout_time = time.time() + 5
                    block_index = msg_json["block_index"]
                    selection_in_process = True

                node_gen_stakes[msg_json["nodeId"]] = msg_json["stake"]
    

    def mainloop(self):

        while True:

            print("")

            print("Node " + str(self.nodeId) + ":")
            print("    Accured Rewards: " + str(self.accruedRewards))
            print("    Stake: " + str(self.amoutAtStake))
            print("    Leader: " + str(self.isLeader))
            print("")
            print("Please select from the following menu:")
            print("1. Add money to account.") 
            print("2. Send money someone.") 
            print("3. Print blockchain") 
            print("4. Print transaction queue") 
            print("5. Remove transaction from queue") 


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

            elif user_input == "4":
                if len(self.bc.transaction_queue) > 0:
                    print("-"*30)
                    for my_trans in self.bc.transaction_queue:
                        my_trans.print()
                        print("-"*30)
                else:
                    print("No transactions to show")
                continue

            elif user_input == "5":
                which_trans = int(input("Which transaction do you want to remove? "))
                id_to_remove = self.bc.transaction_queue[which_trans].id
                print("Removed transaction " + id_to_remove)
                self.bc.remove_transaction(id_to_remove)
                msg = json.dumps({"type": "RemoveTransaction", "trans_id": id_to_remove})
                self.sqs_instance.send_message_to_all_other_nodes(msg)
                continue

            else:
                continue

            # Send transaction to other nodes
            msg = json.dumps({"type": "Transaction", "data": trans.to_json()})
            self.sqs_instance.send_message_to_all_other_nodes(msg)

            self.bc.transaction_queue.append(trans)
        







    
