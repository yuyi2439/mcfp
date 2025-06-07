from dataclasses import dataclass, field
from typing import Optional, Self

from mcfp.command.commands import CommandBase
from mcfp.command.util import Entity


@dataclass
class Execute(CommandBase):
    then: Optional[CommandBase] = None
    subcommands: list[tuple[str, tuple[str | Entity]]] = field(default_factory=list)

    def __str__(self) -> str:
        execute_str = 'execute'
        for cmd, arg in self.subcommands:
            execute_str += f' {cmd} {' '.join(str(a) for a in arg)}'
        assert (
            self.then is not None
        ), 'Execute command must have a "then" command to run.'
        return f'{execute_str} run {str(self.then)}'

    def run(self, then: CommandBase) -> Self:
        """
        Add a `run` subcommand to the execute command.
        """
        self.then = then
        return self

    def as_(self, selector: Entity) -> Self:
        """
        Add an `as` subcommand to the execute command.
        """
        self.subcommands.append(('as', (selector,)))
        return self

    def at(self, selector: Entity) -> Self:
        """
        Add an `at` subcommand to the execute command.
        """
        self.subcommands.append(('at', (selector,)))
        return self
