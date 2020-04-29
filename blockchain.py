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
        self.pendingTransactions = list()
    
    #(self, index, nonce, timestamp,.pendingTransactions, prevHash, numberOfZeros, signed='')
    def createGenesisBlock(self): 
        return Block(0, 1, datetime.datetime.utcnow(), 'genesis', 0, 0, True)
    
    def addBlockToChain(self, nonce, pendingTransactions, numberOfZeros, signed):
        prevHash = getPrevHash()
        self.blocks.append(Block(len(self.blocks), nonce, datetime.datetime.utcnow(), pendingTransactions, prevHash, numberOfZeros, signed))

    def createChainIfDoesNotExist(self):
        if not os.path.isfile(self.blockchainFile):
            file = open(self.blockchainFile, 'w')
            file.close()
    
    def getPrevHash(self):
        latestBlock = self.blocks.pop()
        return latestBlock.getBloc.pendingTransactions['hash']

    # does not include genesis block
    def getLength(self): 
        return len(self.blocks)-1

    def addpendingTransactions(self,pendingTransaction):

        self.pendingTransactions.append(pendingTransaction)
        print(self.pendingTransactions)



