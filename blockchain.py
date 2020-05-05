from block import Block
import datetime
import os
from transaction import Transaction
import json
import time
from typing import *
from sqs_recieve import Sqs
import threading


class Blockchain:

    # when initalizing create a genesis block
    def __init__(self, blockchainFile: str, num_zeroes=5):

        self.blockchainFile = blockchainFile
        self.num_zeroes = num_zeroes
        self.blocks = []
        self.is_mining = False
        # self.pendingTransactions = []

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

    # (self, index, nonce, timestamp,.pendingTransactions, prevHash, numberOfZeros, signed='')
    def createGenesisBlock(self):
        gen_block = Block(0, 1, Transaction(), None, True)
        gen_block.hash = "000000000000000000000000000000"
        return gen_block

    # def addBlockToChain(self, nonce, pendingTransactions, numberOfZeros, signed):
    #     prevHash = getPrevHash()
    #     block_to_append = Block(len(self.blocks), nonce, datetime.datetime.utcnow(), pendingTransactions, prevHash, numberOfZeros, signed)
    #     self.blocks.append(block_to_append)
    #     self.writeBlockToFile(block_to_append)

    def addBlockToChain(self, block: Block):

        if block.prevHash != self.getPrevHash():
            print("Block prevhash not matchin my prevhash!!!")
            return False

        self.blocks.append(block)
        return True


    def getPrevHash(self):
        return self.blocks[-1].hash

    # does not include genesis block
    # def getLength(self):
    #     return len(self.blocks)-1

    # def addpendingTransactions(self,pendingTransaction):

    #     self.pendingTransactions.append(pendingTransaction)
    #     print(self.pendingTransactions)

    def print(self):
        for block in self.blocks:
            print(block)

    def mineTransaction(self, trans: Transaction):

        block = Block(len(self.blocks), 1, trans, self.getPrevHash())
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

