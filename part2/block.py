import hashlib
import json
import datetime
from dateutil import parser
from typing import *
import sys
sys.path.append("../")
from transaction import Transaction

class Block:
    def __init__(self, index, data: Transaction, prevHash, creator_id):

        self.index = index
        self.data = data
        self.prevHash = prevHash
        self.creator_id = creator_id

        self.hash = self.hashBlock()
        self.verifiers = []
        self.creator_reward = 2
        self.verifier_reward = 1

    def add_verifier(self, verifier_id):
        self.verifiers.append(verifier_id)

    def get_rewards(self, node_id):

        total = 0

        if node_id == self.creator_id:
            total += self.creator_reward

        if node_id in self.verifiers:
            total += self.verifier_reward

        return total

    # hashes itself with SHA256 and assigns value
    def hashBlock(self):
        sha_protocol = hashlib.sha256()
        sha_protocol.update(
            str(self.index).encode('utf-8') +
            str(self.data.to_json()).encode('utf-8') +
            str(self.prevHash).encode('utf-8'))
        return sha_protocol.hexdigest()

    def to_json(self):
        block_dict = self.__dict__.copy()
        block_dict["data"] = block_dict["data"].to_json()
        return json.dumps(block_dict)


    @classmethod
    def from_json(cls, json_str):
        arg_dict = json.loads(json_str)
        arg_dict["data"] = Transaction.from_json(arg_dict["data"])

        hash = arg_dict.pop("hash")
        verifiers = arg_dict.pop("verifiers")
        arg_dict.pop("verifier_reward")
        arg_dict.pop("creator_reward")

        block_obj = cls(**arg_dict)
        block_obj.hash = hash
        block_obj.verifiers = verifiers
        return block_obj

    def __str__(self):
        obj_dict = self.__dict__.copy()
        print(obj_dict["data"])
        obj_dict["data"] = obj_dict["data"].__str__()
        return json.dumps(self.__dict__)

    def print(self):
        print("Block: " + str(self.index))
        print("Nonce: " + str(self.nonce))
        self.data.print()
        print("PrevHash: " + str(self.prevHash))
        print("Hash: " + self.hash)


if __name__ == "__main__":
    trans = Transaction()
    trans.add_transfer("hoy", "anna", 20)
    myblock = Block(1, trans, "000000000000", 0)

    json_string = myblock.to_json()
    print(json_string)

    myblock2 = Block.from_json(json_string)

    myblock.add_verifier(1)

    print(myblock.get_rewards(0))
    print(myblock.get_rewards(1))

