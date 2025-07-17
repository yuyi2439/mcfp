from contextlib import contextmanager
from pathlib import Path

import mcfp


class Collecter:
    commands: list[str] = []
    _collecting = False

    @classmethod
    def add_command(cls, command: str):
        cls.commands.append(command)

    @classmethod
    def save_commands(cls, relative_fpath: str):
        """Save collected commands to a file."""
        target_path = mcfp.TargetPath.get() / mcfp.NameSpace.get() / 'function' / Path(relative_fpath)

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(
            '\n'.join([cmd for cmd in cls.commands]), encoding='utf8'
        )
        cls.commands.clear()

    @classmethod
    @contextmanager
    def collect(cls):
        cls._collecting = True
        try:
            yield
        finally:
            cls._collecting = False

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
