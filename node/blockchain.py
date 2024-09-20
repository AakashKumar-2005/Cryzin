from datetime import datetime
import hashlib
from config import GENESIS, MINE_RATE, INITIAL_DIFFICULTY


cryptohash = lambda s: hashlib.sha256(s.encode()).hexdigest()


class Block:
    def __init__(
        self,
        lasthash: str,
        timestamp: int,
        difficulty: int,
        data,
        nonce: int,
        hash: str = None,
    ) -> None:
        self.lasthash = lasthash
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.data = data
        self.nonce = nonce
        self.hash = hash

    @classmethod
    def genesis(cls):
        block = cls(
            lasthash=None,
            timestamp=0,
            difficulty=INITIAL_DIFFICULTY,
            data={"candidates": GENESIS},
            nonce=0,
        )
        block.hash = cryptohash(str(block))
        return block

    def __str__(self) -> str:
        return (
            f"{self.lasthash}{self.timestamp}{self.difficulty}{self.data}{self.nonce}"
        )

    def __dict__(self):
        return {
            "lasthash": self.lasthash,
            "timestamp": self.timestamp,
            "difficulty": self.difficulty,
            "data": self.data,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    @staticmethod
    def validate(block):
        return block.hash == cryptohash(str(block))

    @classmethod
    def mine_block(cls, lastblock, data):
        nonce = 0
        difficulty = lastblock.difficulty
        while True:
            nonce += 1
            timestamp = datetime.timestamp(datetime.now())
            difficulty = Block.adjust_difficulty(
                originalblock=lastblock, timestamp=timestamp
            )
            hash = cryptohash(f"{lastblock.hash}{timestamp}{difficulty}{data}{nonce}")
            if hash[:difficulty] == "0" * difficulty:
                print(hash)
                return cls(
                    lasthash=lastblock.hash,
                    timestamp=timestamp,
                    difficulty=difficulty,
                    data=data,
                    nonce=nonce,
                    hash=hash,
                )

    @staticmethod
    def adjust_difficulty(originalblock, timestamp):
        if originalblock.difficulty < 1:
            return 1
        if (timestamp - originalblock.timestamp) > MINE_RATE:
            return originalblock.difficulty - 1
        return originalblock.difficulty + 1


class Blockchain:
    def __init__(self) -> None:
        self.chain = [Block.genesis()]

    def replace_chain(self, chain):
        if len(chain) <= len(self.chain):
            print("The incoming chain must be longer")
            return
        if not Blockchain.is_valid_chain(chain):
            print("The incoming chain must be valid")
            return
        print("replacing chain")
        self.chain = chain

    @staticmethod
    def is_valid_chain(chain):
        if chain[0] != Block.genesis():
            return False
        for i in range(1, len(chain)):
            if chain[i].lasthash != chain[i - 1].hash:
                return False
            if (
                cryptohash(
                    f"{chain[i].hash}{chain[i].timestamp}{chain[i].difficulty}{chain[i].data}{chain[i].nonce}"
                )
                != chain[i].hash
            ):
                return False
            return True

    def add_block(self, data):
        self.chain.append(Block.mine_block(lastblock=self.chain[-1], data=data))