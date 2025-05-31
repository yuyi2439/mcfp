from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Selector:
    target: str
    arguments: Optional[dict] = None

    def __str__(self):
        if not self.arguments:
            return f"@{self.target}"
        args = ",".join([f"{k}={v}" for k, v in self.arguments.items()])
        return f"@{self.target}[{args}]"


@dataclass
class Position:
    x: int | str
    y: int | str
    z: int | str

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


@dataclass
class Var(Generic[T]):
    """
    True variable that is used in mcfunctions.
    """
    inner: T


@dataclass
class Return(Generic[T]):
    """
    Commmand return
    """
    success: bool
    result: Optional[Var[T]] = None
