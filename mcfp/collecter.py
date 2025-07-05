import inspect
from contextlib import contextmanager
from pathlib import Path


class Collecter:
    commands: list[str] = []
    _collecting = False

    @classmethod
    def add_command(cls, command: str):
        cls.commands.append(command)

    @classmethod
    def save_commands(cls, filename: str | None = None):
        """save collected commands to a file.

        Args:
            filename (str, optional): filename('mcfunction' as suffix). Defaults to the filename of the caller.
        """
        if filename is None:
            filename = inspect.currentframe().f_back.f_code.co_filename  # type: ignore
            filename = filename.replace('.py', '.mcfunction')

        fpath = Path(filename)
        target_path = fpath.parent / 'target' / fpath.name
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
