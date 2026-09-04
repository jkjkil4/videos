# ruff: noqa
from janim.imports import *


class Test(Timeline):
    def construct(self) -> None:
        Square().show()
