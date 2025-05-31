

from dataclasses import dataclass
from typing import Optional


@dataclass
class Selector:
    target: str
    arguments: Optional[dict] = None

    def __str__(self):
        if not self.arguments:
            return f"@{self.target}"
        args = ",".join([f"{k}={v}" for k, v in self.arguments.items()])
        return f"@{self.target}[{args}]"