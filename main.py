import sys
import json
import threading
import random
import time
from blockchain import blockchain
import sqs_recieve

if __name__ == "__main__":

    # i don't know if we want to use this
    node_id = int(sys.argv[1])

    with open('ec2_setup.json') as f:
        CONFIG = json.load(f)

    BCoin = blockchain()

    print('################################################\n')
    print('###########    Blockchain Started    ###########\n')
    print('################################################\n')

    while True:
        #message_recieved = sqs_recieve.retrieve_sqs_messages()
        #if message_recieved != None:
        #    pass
        BCoin.createChainIfDoesNotExist()
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
            