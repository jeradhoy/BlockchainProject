from block import Block
import datetime, os, typing
from typing import *
import sys
sys.path.append("../")
from transaction import Transaction

class Blockchain:

    # when initalizing create a genesis block
    def __init__(self, blockchainFile: str): 

        self.blockchainFile = blockchainFile
        self.blocks = []
        self.transaction_queue = []

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
            f.write(block_to_write.to_json() + "\n")

    def createGenesisBlock(self):
        gen_block = Block(0, Transaction(), None, True)
        gen_block.hash = "000000000000000000000000000000"
        return gen_block

    def check_no_double_spending(self, block: Block):

        # Check each transaction
        for trans in block.data.trans:

            account_name = trans["from"]
            account_balance_needed = trans["amt"]
            account_balance = 0

            #-------------------
            # Check against other transactions in the block
            for concurrent_trans in block.data.trans:
                if concurrent_trans.id != trans.id:

                    # Account received money, increase balance
                    if concurrent_trans["to"] == account_name:
                        account_balance += concurrent_trans["amt"]

                    # Account sent money, decrease balance
                    if concurrent_trans["from"] == account_name:
                        account_balance -= concurrent_trans["amt"]

            for concurrent_coinbase in block.data.coinbase:

                if concurrent_coinbase["account"] == account_name:
                    account_balance += concurrent_coinbase["amt"]
            #-------------------------


            # Look through blocks in reverse
            for prev_block in self.blocks[::1]:

                for prev_trans in prev_block.data.trans:

                    # Account received money, increase balance
                    if prev_trans["to"] == account_name:
                        account_balance += prev_trans["amt"]

                    # Account sent money, decrease balance
                    if prev_trans["from"] == account_name:
                        account_balance -= prev_trans["amt"]

                for prev_coinbase in prev_block.data.coinbase:

                    # Account added money, increase balance
                    if prev_coinbase["account"] == account_name:
                        account_balance += prev_coinbase["amt"]

                if account_balance > account_balance_needed:
                    return True

            return False

        # Not transactions, nothing to verify
        return True

    def verifyBlock(self, block: Block):

        if block.prevHash != self.getPrevHash():
            print("Block prevhash not matchin my prevhash!!!")
            return False
        
        if not self.check_no_double_spending(block):
            print("Double spending found!!!")
            return False

        return True
    
    def addBlockToChain(self, block: Block):

        self.blocks.append(block)
        self.writeBlockToFile(block)
        return True

    def getPrevHash(self):
        latestBlock = self.blocks[-1]
        return latestBlock.hash

    # does not include genesis block
    def getPrevHash(self):
        return self.blocks[-1].hash

    def getLength(self): 
        return len(self.blocks)-1

    def print(self):
        print("-"*30)
        for block in self.blocks:
            block.print()
            print("-"*30)




    # def addpendingTransactions(self,pendingTransaction):

    #     self.pendingTransactions.append(pendingTransaction)
    #     print(self.pendingTransactions)

if __name__ == "__main__":

    bc = Blockchain("blockchain_test.txt")
