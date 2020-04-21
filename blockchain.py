import block
import datetime

class blockchain:
    # when initalizing create a genesis block
    def __init__(self): 
        self.blocks = [self.genesisBlock()]
    
    #(self, index, nonce, timestamp, data, prevHash, numberOfZeros, signed='')
    def genesisBlock(self): 
        return block(0, 1, datetime.datetime.utcnow(), 'genesis', 0, 0, True)
    
    def addBlockToChain(self, nonce, data, numberOfZeros, signed):
        prevHash = getPrevHash()
        self.blocks.append(block(len(self.blocks), nonce, datetime.datetime.utcnow(), data, prevHash, numberOfZeros, signed)
    
    def getPrevHash(self):
        latestBlock = self.blocks.pop()
        return latestBlock.getBlockData['hash']

    # does not include genesis block
    def getLength(self): 
        return len(self.blocks)-1
