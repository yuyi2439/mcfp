from mcfp import NameSpace
from mcfp.command.commands import Function


class Var:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name


class List(list):
    def __init__(self, name: str, *args):
        super().__init__(*args)
        self.name = name

    def len(self):
        return Function(
            'built_in/utils/list_len',
            args={'namespace': NameSpace.get(), 'list_name': self.name},
            namespace='mcfp_gen',
        )
