from block import Block
import datetime
import os
from transaction import Transaction
import json
import time
from typing import *
import threading


class Blockchain:

    # when initalizing create a genesis block
    def __init__(self, blockchainFile: str, num_zeroes=6):

        self.blockchainFile = blockchainFile
        self.num_zeroes = num_zeroes
        self.blocks = []
        # self.pendingTransactions = []

        if os.path.isfile(self.blockchainFile):

            # Read blocks from file
            self.build_chain_from_file(self.blockchainFile)

        else:
            genesisBlock = self.createGenesisBlock()
            self.blocks.append(genesisBlock)
            self.writeBlockToFile(genesisBlock)
        
        self.transaction_queue = []

    def build_chain_from_file(self, blockchainFile):

        with open(blockchainFile, "r") as f:
            lines = f.readlines()

        for line in lines:
            block_to_add = Block.from_json(line)
            self.blocks.append(block_to_add)

    def writeBlockToFile(self, block_to_write: Block):

        with open(self.blockchainFile, "a") as f:
            f.write(block_to_write.to_json() + "\n")

    # (self, index, nonce, timestamp,.pendingTransactions, prevHash, numberOfZeros, signed='')
    def createGenesisBlock(self):
        gen_block = Block(0, 1, Transaction(), None, True)
        gen_block.hash = "000000000000000000000000000000"
        return gen_block

    def check_no_double_spending(self, block: Block):

        # Check each transaction
        for trans in block.data.trans:

            account_name = trans["from"]
            account_balance_needed = trans["amt"]
            account_balance = 0

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



    def addBlockToChain(self, block: Block):

        if block.prevHash != self.getPrevHash():
            print("Block prevhash not matchin my prevhash!!!")
            return False
        
        if not block.hash.startswith("0"*self.num_zeroes):
            print("Block has not met the difficulty set!!!")
            return False

        if not self.check_no_double_spending(block):
            print("Double spending found!!!")
            return False

        self.blocks.append(block)
        self.writeBlockToFile(block)
        return True


    def getPrevHash(self):
        return self.blocks[-1].hash


    def print(self):
        print("-"*30)
        for block in self.blocks:
            block.print()
            print("-"*30)

    def miningLoop(self):

        while True:

            if len(self.transaction_queue) == 0:
                continue

            trans = self.transaction_queue.pop(0)

            self.mineTransaction(trans)

    def mineTransaction(self, trans: Transaction):

        block = Block(len(self.blocks), 1, trans, self.getPrevHash())

        if not self.check_no_double_spending(block):
            print("Double spending found!!! Not mining block!")
            return False

        print("Mining block: " + block.to_json())

        while block.prevHash == self.getPrevHash():

            if block.hash.startswith("0"*self.num_zeroes):
                block.signed == True
                print("Mined block " + str(block.index) +
                      " with nonce of " + str(block.nonce))
                success = self.addBlockToChain(block)

                if success:
                    return True
                else:
                    return False

            block.increment_nonce()

        print("Blockchain grew while mining, terminating!")


if __name__ == "__main__":

    blockchain = Blockchain("blockchain_test.txt", num_zeroes=4)
    trans = Transaction(coinbase=[{"amt": 100, "account": "hoy"}])
    blockchain.mineTransaction(trans)
    blockchain.print()
    trans2 = Transaction(trans=[{"from": "hoy", "to": "watson", "amt": 50}])
    blockchain.mineTransaction(trans2)
    blockchain.print()

