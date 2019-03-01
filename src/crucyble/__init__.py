import logging

from crucyble.glove import GloVe
from crucyble.stages import *

logging.basicConfig(level=logging.DEBUG)

Stage.glove = GloVe