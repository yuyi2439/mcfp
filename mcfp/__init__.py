from pathlib import Path

DEBUG = False


class NameSpace:
    namespace = 'mcfp_generated'

    @classmethod
    def set(cls, namespace: str):
        cls.namespace = namespace

    @classmethod
    def get(cls) -> str:
        return cls.namespace


class TargetPath:
    target_path = Path('.target')

    @classmethod
    def set(cls, path: Path, patch: bool = True):
        cls.target_path = path / '.target' if patch else path

    @classmethod
    def get(cls) -> Path:
        return cls.target_path


__version__ = (0, 1, 4)
