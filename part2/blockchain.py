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
        self.transaction_queue: List[Transaction] = []

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
        gen_block = Block(0, [Transaction()], None, True)
        gen_block.hash = "000000000000000000000000000000"
        return gen_block

    def check_no_double_spending(self, block: Block):

        # No transactions, nothing to verfy
        if len(block.data) == 0:
            return True

        # Check each transaction
        for i, trans in enumerate(block.data):

            # No transfers, move on
            if trans.transfer is None:
                continue

            account_name = trans.transfer["from"]
            account_balance_needed = trans.transfer["amt"]
            account_balance = 0

            #-------------------
            # Check against other transactions in the block
            for j, concurrent_trans in enumerate(block.data):

                if i != j:

                    if concurrent_trans.transfer is not None:

                        # Account received money, increase balance
                        if concurrent_trans.transfer["to"] == account_name:
                            account_balance += concurrent_trans.transfer["amt"]

                        # Account sent money, decrease balance
                        if concurrent_trans.transfer["from"] == account_name:
                            account_balance -= concurrent_trans.transfer["amt"]
                    
                    if concurrent_trans.coinbase is not None:

                        if concurrent_trans.coinbase["account"] == account_name:
                            account_balance += concurrent_trans.coinbase["amt"]
            #-------------------------

            # Look through blocks in reverse
            for prev_block in self.blocks[::1]:

                if account_balance > account_balance_needed:
                    break

                for prev_trans in prev_block.data:

                    if prev_trans.transfer is not None:

                        # Account received money, increase balance
                        if prev_trans.transfer["to"] == account_name:
                            account_balance += prev_trans.transfer["amt"]

                        # Account sent money, decrease balance
                        if prev_trans.transfer["from"] == account_name:
                            account_balance -= prev_trans.transfer["amt"]

                    if prev_trans.coinbase is not None:

                        # Account added money, increase balance
                        if prev_trans.coinbase["account"] == account_name:
                            account_balance += prev_trans.coinbase["amt"]

            # Looked through every block, compare accounts
            if account_balance < account_balance_needed:
                return False

        # No issues found!
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

        
        commited_uuids = [trans.id for trans in block.data]
        self.transaction_queue = [trans for trans in self.transaction_queue if trans.id not in commited_uuids]

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


if __name__ == "__main__":

    bc = Blockchain("blockchain_test.txt")
