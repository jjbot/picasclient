"""PiCaS: Pitch Catch System

.. moduleauthor:: Jan Bot <janjbot@gmail.com>

A module to work through large amounts of jobs on heterogeneous compute
infrastructure. Relies on a CouchDB server to keep track of the work itself.

"""

import logging
from .documents import Document, Task, Job, User
from .clients import CouchDB
from .iterators import (ViewIterator, TaskViewIterator, EndlessViewIterator,
                        PrioritizedViewIterator)
from .actors import RunActor


version = 0.50

picaslogger = logging.getLogger("PiCaS")
formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
picaslogger.addHandler(ch)
picaslogger.setLevel(logging.ERROR)

__all__ = [
    'CouchDB',
    'Document',
    'EndlessViewIterator',
    'Job',
    'PrioritizedViewIterator',
    'RunActor',
    'Task',
    'TaskViewIterator',
    'User',
    'ViewIterator',
]
