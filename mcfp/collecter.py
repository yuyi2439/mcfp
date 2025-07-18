from contextlib import contextmanager
from pathlib import Path

import mcfp
from mcfp import command as command
from mcfp.command.util import Storage
from mcfp.data_struct import Var


class Collecter:
    cmds: list[str] = []
    _collecting = False

    @classmethod
    def add_command(cls, cmd: str):
        cls.cmds.append(cmd)

    @classmethod
    def save_commands(cls, relative_fpath: str):
        """Save collected commands to a file."""
        target_path = (
            mcfp.TargetPath.get()
            / mcfp.NameSpace.get()
            / 'function'
            / Path(relative_fpath)
        )

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(
            '\n'.join([cmd for cmd in cls.cmds]), encoding='utf8'
        )
        cls.cmds.clear()

    @classmethod
    @contextmanager
    def collect(cls):
        cls._collecting = True
        try:
            yield
        finally:
            cls._collecting = False

    @classmethod
    def try_collect_command(cls, cmd: object):

        if cls._collecting:
            if isinstance(cmd, command.CommandBase):
                cls.add_command(str(cmd))
            else:
                pass
        else:
            raise RuntimeError(
                "Collecter is not collecting commands. Use Collecter.collect() context manager to enable command collection."
            )
    
    @classmethod
    def collect_assign(cls, target: Var, value: command.CommandBase):
        # 暂时只处理简单的赋值
        if isinstance(value, command.CommandBase):
            if isinstance(target, Var):
                cmd = command.Execute().store(Storage('var'), target.name).run(value)
                cls.add_command(str(cmd))
