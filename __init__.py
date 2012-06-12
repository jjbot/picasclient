"""PiCaS: Pitch Catch System

.. moduleauthor:: Jan Bot <janjbot@gmail.com>

"""

import logging
from logging import StreamHandler

version = 0.30

picaslogger = logging.getLogger("PiCaS")
formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
picaslogger.addHandler(ch)
picaslogger.setLevel(logging.ERROR)