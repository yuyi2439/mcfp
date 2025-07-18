import json
from dataclasses import dataclass
from functools import singledispatch
from typing import Iterable, Optional

from mcfp import NameSpace
from mcfp.command.util import Position, Selector


class CommandBase:
    def __str__(self) -> str:
        raise NotImplementedError('Subclasses must implement __str__ method')

    def __call__(self):
        from mcfp.collecter import Collecter

        Collecter.add_command(str(self))


@dataclass
class Command(CommandBase):
    command: str
    args: Optional[Iterable[str]]

    def __str__(self) -> str:
        return f'{self.command} {' '.join(self.args) if self.args else ''}'.strip()


@dataclass
class SetBlock(CommandBase):
    pos: Position
    block: str
    state: str = ''
    mode: str = 'replace'

    def __str__(self) -> str:
        state_str = f'[{self.state}]' if self.state else ''
        return f'setblock {str(self.pos)} {self.block}{state_str} {self.mode}'


@dataclass
class Function(CommandBase):
    name: str
    args: dict[str, str] | None = None
    namespace: str = NameSpace.get()

    def __str__(self) -> str:
        cmd = f'function {self.namespace}:{self.name}'
        if self.args:
            args_str = json.dumps(self.args)
            cmd += f' {args_str}'
        return cmd


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
        if self.operation == 'players':
            return f'scoreboard players {self.operation} {self.target} {self.objective}'
        elif self.operation in ['set', 'add', 'remove']:
            return f'scoreboard players {self.operation} {self.target} {self.objective} {self.source}'
        elif self.operation in ['operation']:
            return (
                f'scoreboard players {self.operation} {self.target} {self.objective} '
                f'{self.operation} {self.source} {self.source_objective}'
            )
        else:
            raise ValueError(f'Invalid scoreboard operation: {self.operation}')


@singledispatch
def setblock(arg, *args, **kwargs) -> SetBlock:
    raise TypeError("不支持的参数类型")


@setblock.register
def _(pos: Position, block: str, state: str = '', mode: str = 'replace'):
    return SetBlock(pos, block, state, mode)


@setblock.register
def _(pos_tuple: tuple, block: str, state: str = '', mode: str = 'replace'):
    if len(pos_tuple) != 3:
        raise TypeError("坐标tuple长度必须为3")
    return SetBlock(Position(*pos_tuple), block, state, mode)


@setblock.register
def _(x: int, y: int, z: int, block: str, state: str = '', mode: str = 'replace'):
    return SetBlock(Position(x, y, z), block, state, mode)


__all__ = [
    'Command',
    'setblock',
    'Function',
    'Say',
    'Scoreboard',
]
