import hashlib
import json
import datetime
from dateutil import parser

class Block:
    def __init__(self, index, nonce, timestamp, data, prevHash, numberOfZeros, signed=''):
        self.index = index
        self.nonce = nonce
        self.timestamp = timestamp
        self.data = data
        self.prevHash = prevHash
        self.numberOfZeros = numberOfZeros
        self.hash = self.hashBlock()
        self.signed = signed

    # hashes itself with SHA256 and assigns value
    def hashBlock(self):
        sha_protocol = hashlib.sha256()
        sha_protocol.update(
            str(self.index).encode('utf-8')+
            str(self.nonce).encode('utf-8')+
            str(self.timestamp).encode('utf-8')+
            str(self.data).encode('utf-8')+
            str(self.prevHash).encode('utf-8')+
            str(self.numberOfZeros).encode('utf-8'))
        return sha_protocol.hexdigest()

    def getBlockData(self):
        blockData = {'index': self.index, 'nonce':self.nonce, 'timestamp':self.timestamp,
                        'data':self.data, 'prevHash':self.prevHash,
                        'numberOfZeros':self.numberOfZeros, 'hash':self.hash, 'signed':self.signed}

        return blockData

    def to_json(self):
        block_dict = self.__dict__
        block_dict["timestamp"] = str(block_dict["timestamp"])
        return json.dumps(block_dict)

    @classmethod
    def from_json(cls, json_str):
        arg_dict = json.loads(json_str)
        hash = arg_dict.pop("hash")
        arg_dict["timestamp"] = parser.parse(arg_dict["timestamp"])
        block_obj = cls(**arg_dict)
        block_obj.hash = hash
        return block_obj


if __name__ == "__main__":
    myblock = Block(1, 2, 3, "emow", 234234234, 4)
    json_string = myblock.to_json()
    myblock2 = Block.from_json(json_string)
    print(myblock.__dict__)
    print(myblock2.__dict__)
