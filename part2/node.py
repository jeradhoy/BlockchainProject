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
    def __init__(self, nodeId, amoutAtStake):

        self.nodeId = nodeId
        self.amoutAtStake = amoutAtStake
        # self.sqs_instance = sqs_instance

        self.accruedRewards = 0
    

        # means that they can select who creates the block
        self.isLeader = False

        # means that they can create the block
        self.isCreator = False

        self.bc = Blockchain("verifier_" + str(id) + ".txt")

        # put dummie values in this for now for testing
        self.totalAtStakeDict = {0: 1000, 1: 2000, 3: 3000, 4: 500}
        # self.atStakeDict = {}
        # self.atStakeDict[nodeId] = amoutAtStake

        self.stakeArray = []

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
        







    
