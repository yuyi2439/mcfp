from dataclasses import dataclass
from typing import Iterable, Optional

from mcfp.command.util import Position, Selector
from mcfp.compiler import Compiler


class CommandBase:
    def __str__(self) -> str:
        raise NotImplementedError("Subclasses must implement __str__ method")

    def __call__(self):
        Compiler.add_command(str(self))


@dataclass
class Command(CommandBase):
    command: str
    args: Optional[Iterable[str]]

    def __str__(self) -> str:
        return f"{self.command} {' '.join(self.args) if self.args else ''}".strip()


@dataclass
class SetBlock(CommandBase):
    pos: Position
    block: str
    state: str = ""
    mode: str = "replace"

    def __str__(self) -> str:
        state_str = f"[{self.state}]" if self.state else ""
        return f"setblock {str(self.pos)} {self.block}{state_str} {self.mode}"


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
    'Command',
    'SetBlock',
    'Function',
    'Say',
    'Scoreboard',
]
