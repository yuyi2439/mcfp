from dataclasses import dataclass

from mcfp.command.commands import CommandBase
from mcfp.command.util import Target


@dataclass
class Data(CommandBase):
    target: Target
    sub_cmd: str = 'modify'
    path: str | None = None
    args: list[str] | None = None

    def __str__(self) -> str:
        return f'data {self.sub_cmd} {str(self.target)} {self.path} {" ".join(self.args) if self.args else ""}'.strip()
