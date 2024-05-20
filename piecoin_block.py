import hashlib as hasher

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_bloc()
    
    def hash_bloc(self):
        sha = hasher.sha256()
        sha.update(str(self.index)
                 + str(self.timestamp)
                 + str(self.data)
                 + str(self.previous_hash))
        
        return sha.hexdigest()