from block import Block
import datetime, os

class Blockchain:

    # when initalizing create a genesis block
    def __init__(self, blockchainFile: str): 

        self.blockchainFile = blockchainFile
        self.blocks = []
        self.pendingTransactions = []

        if os.path.isfile(self.blockchainFile):

            # Read blocks from file
            self.build_chain_from_file(self.blockchainFile)

        else:
            genesisBlock = self.createGenesisBlock()
            self.blocks.append(genesisBlock)
            self.writeBlockToFile(genesisBlock)

    def build_chain_from_file(self, blockchainFile):

        with open(blockchainFile, "r") as f:
            lines = f.readlines()

        for line in lines:
            block_to_add = Block.from_json(line)
            self.blocks.append(block_to_add)
    
    def writeBlockToFile(self, block_to_write: Block):

        with open(self.blockchainFile, "a") as f:
            f.write(block_to_write.to_json())

    #(self, index, nonce, timestamp,.pendingTransactions, prevHash, numberOfZeros, signed='')
    def createGenesisBlock(self): 
        return Block(0, 1, datetime.datetime.utcnow(), 'genesis', 0, 0, True)
    
    def addBlockToChain(self, nonce, pendingTransactions, numberOfZeros, signed):
        prevHash = getPrevHash()
        block_to_append = Block(len(self.blocks), nonce, datetime.datetime.utcnow(), pendingTransactions, prevHash, numberOfZeros, signed)
        self.blocks.append(block_to_append)
        self.writeBlockToFile(block_to_append)

    def getPrevHash(self):
        latestBlock = self.blocks[-1]
        return latestBlock.hash

    # does not include genesis block
    def getLength(self): 
        return len(self.blocks)-1

    def addpendingTransactions(self,pendingTransaction):

        self.pendingTransactions.append(pendingTransaction)
        print(self.pendingTransactions)



