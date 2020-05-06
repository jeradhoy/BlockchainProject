from blockchain import Blockchain

class Node:
    def __init__(self, id, amoutAtStake):

        self.amoutAtStake = amoutAtStake

        # means that they can select who creates the block
        self.isLeader = False

        # means that they can create the block
        self.isCreator = False

        self.bc = Blockchain("verifier_" + str(id) + ".txt")



    
