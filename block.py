import hashlib

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