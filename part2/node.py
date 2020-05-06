class node:
    def __init__(self, amoutAtStake):
        self.amoutAtStake = amoutAtStake
        # means that they can select who creates the block
        self.isLeader = False
        # means that they can create the block
        self.isCreator = False

    
