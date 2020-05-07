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

if __name__ == "__main__":

    node_id = int(sys.argv[1])
    amountToStake = int(sys.argv[2])
    verbose = int(sys.argv[3])

    with open('../ec2_setup.json') as f:
        CONFIG = json.load(f)

    mySqs = Sqs(CONFIG, node_id)

    # create node
    myNode = Node(node_id, amountToStake, mySqs, verbose)

    receiveThread = threading.Thread(target = myNode.receive_loop)
    receiveThread.start()
    
    blockThread = threading.Thread(target = myNode.create_block_loop)
    blockThread.start()

    leaderThread = threading.Thread(target = myNode.leader_loop)
    leaderThread.start()

    myNode.mainloop()