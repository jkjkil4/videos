# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *

with reloads():
    from utils.template import *
from utils.template import *


class TL1(Template):
    def construct(self):
        img = ImageItem('glm.png')
