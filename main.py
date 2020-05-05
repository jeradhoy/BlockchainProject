import sys
import json
import threading
import random
import time
from blockchain import Blockchain
from sqs_recieve import Sqs
from transaction import Transaction
from typing import *
from block import Block


class Client:

    def __init__(self, node_id, sqs_config):

        self.sqs_instance = Sqs(sqs_config, node_id)
        self.blockchain = Blockchain("blockchain_" + str(node_id) + ".txt")

        print('################################################\n')
        print('###########    Blockchain Started    ###########\n')
        print('################################################\n')

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
                self.blockchain.print()
                continue

            else:
                continue

            # Send transaction to other nodes
            msg = json.dumps({"Transaction": trans.to_json()})
            self.sqs_instance.send_message_to_all_other_nodes(msg)

            # Start mining block
            threading.Thread(target = self.blockchain.mineTransaction, args=[trans]).start()

    def listen(self):

        lastHash = self.blockchain.getPrevHash()

        while True:

            lastBlock: Block = self.blockchain.blocks[-1]

            # A new block has been mined!
            if lastBlock.hash != lastHash:
                msg = json.dumps({"MinedBlock": lastBlock.to_json()})
                self.sqs_instance.send_message_to_all_other_nodes(msg)
                lastHash = lastBlock.hash

            msg = self.sqs_instance.retrieve_sqs_messages()

            if msg == None:
                continue
        
            print(msg)
            msg_json = json.loads(msg)

            if "Transaction" in msg_json.keys(): 

                trans_obj = Transaction.from_json(msg_json["Transaction"])
                threading.Thread(target = self.blockchain.mineTransaction, args=[trans_obj]).start()

            elif "MinedBlock" in msg_json.keys():

                minedBlock = Block.from_json(msg_json["MinedBlock"])
                success = self.blockchain.addBlockToChain(minedBlock)
                if success:
                    lastHash = minedBlock.hash
                

if __name__ == "__main__":

    node_id = int(sys.argv[1])

    with open('ec2_setup.json') as f:
        CONFIG = json.load(f)

    client = Client(node_id, CONFIG)

    # Start listener
    listenerThread = threading.Thread(target = client.listen)
    listenerThread.start()

    client.mainloop()


#message_recieved = sqs_recieve.retrieve_sqs_messages()
#if message_recieved != None:
#    pass

#blockchain.createChainIfDoesNotExist()
# nodes =['n1', 'n2', 'n3']
# while True:
#     firstNode = random.choice(nodes)
#     secondNode = random.choice(nodes)
#     amountToTransfer = random.randint(1,5)
#     if not firstNode == secondNode:
#         break
# input = {'from': firstNode, 'to': secondNode, 'amount': amountToTransfer}
# waitTime = random.randint(5, 15)
# time.sleep(waitTime)
# probability = random.random()
# probabilityString = str(probability)
# print(probabilityString + ' probability')
# if probability < 0.2:
    #     print('\n New Transaction! \n')
    #     print(input)
    #     print('')
    #     blockchain.addpendingTransactions(input)
    #     mySqs.send_message_to_all_other_nodes(input)