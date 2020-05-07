import hashlib
import json
from typing import *
import random

import sys
sys.path.append("../")
from transaction import Transaction

class Block:
    def __init__(self, index, nonce, data: Transaction, prevHash, signed=''):
        self.index = index
        self.nonce = nonce
        self.data = data
        self.prevHash = prevHash
        self.hash = self.hashBlock()
        self.signed = signed

    # hashes itself with SHA256 and assigns value
    def hashBlock(self):
        sha_protocol = hashlib.sha256()
        sha_protocol.update(
            str(self.index).encode('utf-8') +
            str(self.nonce).encode('utf-8') +
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
        block_obj = cls(**arg_dict)
        block_obj.hash = hash
        return block_obj

    def increment_nonce(self):
        # self.nonce += 1
        self.nonce += random.randint(1, 10)
        self.hash = self.hashBlock()

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
    myblock = Block(1, 2, "emow", "234234234")
    json_string = myblock.to_json()
    myblock2 = Block.from_json(json_string)
    print(json_string)
    print(myblock.__dict__)
    print(myblock2.__dict__)
