# flake8: noqa
from janim.utils.reload import reloads

with reloads():
    from template.templates import *
    from template.sweep_rect import SweepRect
from template.templates import *
from template.sweep_rect import SweepRect
