import sys
import json
import threading
import random
import time
from blockchain import blockchain
from sqs_recieve import Sqs
import sqs_recieve

if __name__ == "__main__":

    node_id = int(sys.argv[1])

    with open('ec2_setup.json') as f:
        CONFIG = json.load(f)

    mySqs = Sqs(CONFIG, node_id)

    blockchain = blockchain("blockchain_" + str(node_id) + ".txt")

    print('################################################\n')
    print('###########    Blockchain Started    ###########\n')
    print('################################################\n')

    while True:
        #message_recieved = sqs_recieve.retrieve_sqs_messages()
        #if message_recieved != None:
        #    pass

        #blockchain.createChainIfDoesNotExist()
        nodes =['n1', 'n2', 'n3']
        while True:
            firstNode = random.choice(nodes)
            secondNode = random.choice(nodes)
            amountToTransfer = random.randint(1,5)
            if not firstNode == secondNode:
                break
        input = {'from': firstNode, 'to': secondNode, 'amount': amountToTransfer}
        waitTime = random.randint(5, 15)
        time.sleep(waitTime)
        probability = random.random()
        probabilityString = str(probability)
        print(probabilityString + ' probability')
        if probability < 0.2:
            print('\n New Transaction! \n')
            print(input)
            print('')
            blockchain.addpendingTransactions(input)
            mySqs.send_message_to_all_other_nodes(input)

        '''        while True:

            print("")
            print("Please select from the following menu:")
            print("1. ") 
            print("2. ") 
            print("3. ") 

            print("")

            user_input = input()


            if user_input == "1":

                pass

            if user_input == "2":

                pass

            if user_input == "3":
               
               pass'''
            