from block import Block
import datetime, os

BLOCKCHAINFILE = 'blockchain.txt'

class blockchain:
    # when initalizing create a genesis block
    def __init__(self): 

        directory = os.path.dirname(os.path.realpath(__file__))
        self.blockchainFile = os.path.join(directory, BLOCKCHAINFILE)

        self.createChainIfDoesNotExist()

        if os.stat(self.blockchainFile).st_size == 0:
            self.genesisBlock = self.createGenesisBlock()

        self.blocks = [self.genesisBlock]
    
    #(self, index, nonce, timestamp, data, prevHash, numberOfZeros, signed='')
    def createGenesisBlock(self): 
        return Block(0, 1, datetime.datetime.utcnow(), 'genesis', 0, 0, True)
    
    def addBlockToChain(self, nonce, data, numberOfZeros, signed):
        prevHash = getPrevHash()
        self.blocks.append(Block(len(self.blocks), nonce, datetime.datetime.utcnow(), data, prevHash, numberOfZeros, signed))

    def createChainIfDoesNotExist(self):
        if not os.path.isfile(self.blockchainFile):
            file = open(self.blockchainFile, 'w')
            file.close()
    
    def getPrevHash(self):
        latestBlock = self.blocks.pop()
        return latestBlock.getBlockData['hash']

    # does not include genesis block
    def getLength(self): 
        return len(self.blocks)-1

    def server_ui(self):

        while True:

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
               
               pass
