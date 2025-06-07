import inspect
from contextlib import contextmanager
from typing import Optional


class Collecter:
    commands: list[str] = []
    _collecting = False

    @classmethod
    def add_command(cls, command: str):
        cls.commands.append(command)

    @classmethod
    @contextmanager
    def collect(cls):
        cls._collecting = True
        try:
            yield
        finally:
            cls._collecting = False

    @classmethod
    def save_commands(cls, filename: Optional[str] = None):
        if filename is None:
            filename = inspect.currentframe().f_back.f_code.co_filename  # type: ignore

        filename = filename.replace('.py', '.mcfunction')
        with open(filename, 'w', encoding='utf8') as file:
            for command in cls.commands:
                file.write(command + '\n')

    @classmethod
    def try_collect_command(cls, command: object):
        from mcfp.command.commands import CommandBase

        if cls._collecting:
            if isinstance(command, CommandBase):
                cls.add_command(str(command))
            else:
                pass
        else:
            raise RuntimeError(
                "Collecter is not collecting commands. Use Collecter.collect() context manager to enable command collection."
            )
