from dataclasses import dataclass

from . import Command, Selector


@dataclass
class Execute(Command):
    subcommands: list[tuple[str, str | Selector]]
    then: Command

    def __str__(self) -> str:
        execute_str = "execute"
        for cmd, arg in self.subcommands:
            execute_str += f" {cmd} {arg}"
        return f"{execute_str} run {str(self.then)}"
