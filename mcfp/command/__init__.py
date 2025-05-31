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


class CommandBase:
    def __str__(self) -> str:
        raise NotImplementedError("Subclasses must implement __str__ method")


@dataclass
class Command(CommandBase):
    command: str
    args: Optional[list[str]]

    def __str__(self) -> str:
        return f"{self.command} {' '.join(self.args) if self.args else ''}".strip()


__all__ = [
    'Command',
    'SetBlock',
    'Execute',
    'Function',
    'Say',
    'Scoreboard',
    'Selector',
]
