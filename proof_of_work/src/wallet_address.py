from dataclasses import dataclass

import base58


@dataclass
class WalletAddress:
    address_bytes: bytes

    @property
    def address(self) -> str:
        return base58.b58encode(self.address_bytes).decode('utf-8')
