from dataclasses import dataclass
from typing import Optional

from ..command import CommandBase, Selector


@dataclass
class SetBlock(CommandBase):
    x: int | str
    y: int | str
    z: int | str
    block: str
    state: str = ""
    mode: str = "replace"

    def __str__(self) -> str:
        state_str = f"[{self.state}]" if self.state else ""
        return (
            f"setblock {self.x} {self.y} {self.z} {self.block}{state_str} {self.mode}"
        )


@dataclass
class Function(CommandBase):
    namespace: str
    name: str

    def __str__(self) -> str:
        return f"function {self.namespace}:{self.name}"


@dataclass
class Say(CommandBase):
    message: str

    def __str__(self) -> str:
        return f'say {self.message}'


@dataclass
class Scoreboard(CommandBase):
    operation: str
    objective: str
    target: str | Selector
    source: Optional[str | Selector] = None
    source_objective: Optional[str] = None

    def __str__(self) -> str:
        if self.operation == "players":
            return f"scoreboard players {self.operation} {self.target} {self.objective}"
        elif self.operation in ["set", "add", "remove"]:
            return f"scoreboard players {self.operation} {self.target} {self.objective} {self.source}"
        elif self.operation in ["operation"]:
            return (
                f"scoreboard players {self.operation} {self.target} {self.objective} "
                f"{self.operation} {self.source} {self.source_objective}"
            )
        else:
            raise ValueError(f"Invalid scoreboard operation: {self.operation}")

__all__ = [
    'SetBlock',
    'Function',
    'Say',
    'Scoreboard',
]
