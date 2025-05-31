from typing import Optional
from dataclasses import dataclass

from .others import *
from .execute import Execute


@dataclass
class Selector:
    target: str
    arguments: Optional[dict] = None

    def __str__(self):
        if not self.arguments:
            return f"@{self.target}"
        args = ",".join([f"{k}={v}" for k, v in self.arguments.items()])
        return f"@{self.target}[{args}]"


class Command:
    def __str__(self) -> str:
        raise NotImplementedError()



__all__ = [
    'SetBlock',
    'Execute',
    'Function',
    'Say',
    'Scoreboard',
    'Selector',
]
