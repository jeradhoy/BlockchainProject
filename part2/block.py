import hashlib
import json
import datetime
from dateutil import parser
from typing import *
import sys
sys.path.append("../")
from transaction import Transaction

class Block:
    def __init__(self, index, data: List[Transaction], prevHash, creator_id, totalStaked=None):

        self.index = index
        self.data = data
        self.prevHash = prevHash
        self.creator_id = creator_id

        self.hash = self.hashBlock()
        self.verifiers = []
        self.creator_reward = 2
        self.verifier_reward = 1
        self.totalStaked = 0

    def add_verifier(self, verifier_id):
        self.verifiers.append(verifier_id)

    def get_rewards(self, node_id):

        total = 0

        if node_id == self.creator_id:
            total += self.creator_reward

        if node_id in self.verifiers:
            total += self.verifier_reward

        return total
    
    def get_transaction_total(self):

        total = 0

        for trans in self.data:

            if trans.coinbase is not None:
                total += trans.coinbase["amt"]

            if trans.transfer is not None:
                total += trans.transfer["amt"]
        
        return total


    # hashes itself with SHA256 and assigns value
    def hashBlock(self):
        sha_protocol = hashlib.sha256()
        sha_protocol.update(
            str(self.index).encode('utf-8') +
            str([trans.to_json() for trans in self.data]).encode('utf-8') +
            str(self.prevHash).encode('utf-8'))
        return sha_protocol.hexdigest()

    def to_json(self):
        block_dict = self.__dict__.copy()
        block_dict["data"] = [trans.to_json() for trans in block_dict["data"]]
        return json.dumps(block_dict)


    @classmethod
    def from_json(cls, json_str):
        arg_dict = json.loads(json_str)
        arg_dict["data"] = [Transaction.from_json(trans) for trans in arg_dict["data"]]

        hash = arg_dict.pop("hash")
        verifiers = arg_dict.pop("verifiers")
        arg_dict.pop("verifier_reward")
        arg_dict.pop("creator_reward")

        block_obj = cls(**arg_dict)
        block_obj.hash = hash
        block_obj.verifiers = verifiers
        return block_obj


    def print(self):
        print("Block: " + str(self.index))
        [trans.print() for trans in self.data]
        print("Creator: " + str(self.creator_id))
        print("Verifiers: " + str(self.verifiers))
        print("TotalStaked: " + str(self.totalStaked))
        print("PrevHash: " + str(self.prevHash))
        print("Hash: " + self.hash)


if __name__ == "__main__":
    trans = Transaction()
    trans.add_transfer("hoy", "anna", 20)
    myblock = Block(1, [trans], "000000000000", 0)

    json_string = myblock.to_json()
    print(json_string)

    myblock2 = Block.from_json(json_string)

    myblock.add_verifier(1)

    print(myblock.get_rewards(0))
    print(myblock.get_rewards(1))

