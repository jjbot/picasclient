"""PiCaS: Pitch Catch System
The MIT License (MIT)

Copyright (c) 2016, Jan Bot

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


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