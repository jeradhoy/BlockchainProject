import sys
import json
import threading
import random
import time
from blockchain import Blockchain
from sqs_recieve import Sqs
import sqs_recieve
from node import node

def sortNodes(CONFIG):
    nodes = []
    for node in CONFIG['nodes']:
        node = node['id']
        nodes.append(node)
    nodes.sort()
    return nodes

def declareLeader(nodes):
    leader = nodes[0]
    return leader

def setLeader(leaderNodeId, node_id, myNode):
    if node_id == leaderNodeId:
        myNode.isLeader = True
        print()
        print('##############################################################')
        print('This node has the lowest ID and has been slected as the leader')
        print('##############################################################')
        print()
    else:
        myNode.isLeader = False
        print()
        print('########################################################################')
        print('This node does not have the lowest ID and was no selected as the leader')
        print('########################################################################')
        print()


if __name__ == "__main__":

    node_id = int(sys.argv[1])
    amountToStake = int(sys.argv[2])
    myNode = node(node_id)

    stakeMessage = {'type': 'proofOfStake', 'amount': amountToStake}

    with open('ec2_setup.json') as f:
        CONFIG = json.load(f)
    
    nodes = sortNodes(CONFIG)
    leaderNodeId = declareLeader(nodes)
    setLeader(leaderNodeId, node_id, myNode)
    # if myNode.isLeader:
    #   select which node can create block based on stake and send alert this node of that    

    mySqs = Sqs(CONFIG, node_id)
    mySqs.send_message_to_all_other_nodes(stakeMessage)

    blockchain = Blockchain("blockchain_" + str(node_id) + ".txt")

    print('################################################\n')
    print('###########    Blockchain Started    ###########\n')
    print('################################################\n')

    while True:
        #message_recieved = sqs_recieve.retrieve_sqs_messages()
        #if message_recieved != None:
        #    pass


        #blockchain.createChainIfDoesNotExist()
        while True:
            firstNode = random.choice(nodes)
            secondNode = random.choice(nodes)
            amountToTransfer = random.randint(1,5)
            if not firstNode == secondNode:
                break
        input = {'type': 'transaction', 'from': firstNode, 'to': secondNode, 'amount': amountToTransfer}
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
            if myNode.isCreator == True:
                # we make that block and send that bitch 
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
            