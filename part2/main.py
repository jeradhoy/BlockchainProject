import sys
import json
import threading
import random
import time
from blockchain import Blockchain
from sqs_recieve import Sqs
import sqs_recieve
from node import Node    
sys.path.append("../")
from transaction import Transaction


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
        # then send amount at stake to leader queue

def generate_random_transaction() -> Transaction:

    node_ids = [0, 1, 2, 3]
    from_to = random.sample(node_ids, 2)
    amountToTransfer = random.randint(1,5)
    trans = Transaction()
    trans.add_transfer(from_to[0], from_to[1], amountToTransfer)
    return trans


# def main():

#     ##### Dissss all psuedo code

#     node_id = int(sys.argv[1])
#     amountToStake = int(sys.argv[2])

#     with open('../ec2_setup.json') as f:
#         CONFIG = json.load(f)

#     sqs_instance = Sqs(CONFIG, node_id)

#     # create node
#     myNode = Node(node_id, amountToStake, sqs_instance)

#     #????????????????????????????
#     myNode.elect_leader()

#     #?????????????
#     # Start 
#     leaderThread = threading.Thread(target = myNode.leader_loop)
#     leaderThread.start()

#     # Start listener
#     listenerThread = threading.Thread(target = myNode.listen)
#     listenerThread.start()

#     myNode.mainloop()



if __name__ == "__main__":

    node_id = int(sys.argv[1])
    amountToStake = int(sys.argv[2])

    with open('../ec2_setup.json') as f:
        CONFIG = json.load(f)

    mySqs = Sqs(CONFIG, node_id)

    # create node
    myNode = Node(node_id, amountToStake, mySqs)

    receiveThread = threading.Thread(target = myNode.receive_loop)
    receiveThread.start()
    
    # stakeMessage = {'type': 'proofOfStake', 'amount': amountToStake}
    # # find and declare leader node
    # nodes = sortNodes(CONFIG)
    # leaderNodeId = declareLeader(nodes)
    # setLeader(leaderNodeId, node_id, myNode)

    # mySqs.send_message_to_all_other_nodes(stakeMessage)

    # # if it is leader generate stake array based off others proof of stake
    # if myNode.isLeader:
    #     creatorNode = myNode.pickCreator()

    # blockchain = Blockchain("blockchain_" + str(node_id) + ".txt")

    # print('################################################\n')
    # print('###########    Blockchain Started    ###########\n')
    # print('################################################\n')

    # while True:
    #     #message_recieved = sqs_recieve.retrieve_sqs_messages()
    #     #if message_recieved != None:
    #     #    pass


    #     #blockchain.createChainIfDoesNotExist()
    #     random_transaction = generate_random_transaction()
    #     msg = {"Transaction": random_transaction.to_json()}
        


    #     waitTime = random.randint(5, 15)
    #     time.sleep(waitTime)
    #     probability = random.random()
    #     probabilityString = str(probability)
    #     print(probabilityString + ' probability')
    #     if probability < 0.2:
    #         print('\n New Transaction! \n')
    #         print(msg)
    #         print('')
    #         blockchain.transaction_queue.append(random_transaction)
    #         if myNode.isCreator == True:
    #             # we make that block and send that bitch 
    #             mySqs.send_message_to_all_other_nodes(input)

    #     # if it is leader generate stake array based off others proof of stake
    #     if myNode.isLeader:
    #         creatorNode = myNode.pickCreator()
    #         mySqs.send_msg_to_node(creatorNode, json.dumps({'type':'isCreator'}))