import hashlib
from config import GENESIS


class Block:
    def __init__(self, lasthash, data) -> None:
        self.lasthash = lasthash
        self.data = data
        self.hash = hashlib.sha256(f'{self.lasthash}{data}').hexdigest()


class Blockchain:
    def __init__(self) -> None:
        self.chain = [Block(None, GENESIS)]
