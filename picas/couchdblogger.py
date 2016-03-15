# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2016, Jan Bot

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Created on Mon May 21 16:11:08 2012

@author: Jan Bot
"""

# Python imports
import logging
import random
import socket
import time

# CouchDB imports
from couchdb import Server

class CouchDBLogger(logging.Handler):
    """Logger class which writes messages to CouchDB in a predefined 
    format.
    """
    def __init__(self, url, db):
        """Initiation function.
        :param url: the url including the port on which the database 
        is located.
        :param db: the name of the database.
        """
        logging.Handler.__init__(self)
        self.server = Server(url=url)
        self.db = self.server[db]
        self.hostname = socket.gethostname()
        random.seed(time.time())
        self.trace_nr = int(random.random() * 100000)
    
    def emit(self, record):
        """Function used by the Python logging framework to output messages.
        Internal only.
        :param record: a log-record to process.
        """
        log_dict = {
            'lvl': record.levelno,
            'msg': record.msg,
            'created': record.created,
            'func': record.funcName,
            'host': self.hostname,
            'trance_nr': self.trace_nr,
            'type': 'log'
        }
        
        count = 0
        done = False
        while(count < 10 and not done):
            try:
                id = self.hostname + ":" + str(int(time.time())) 
                self.db[id] = log_dict
                done = True
            except Exception as e:
                print e
                print log_dict
                count += 1
                time.sleep(0.5)

default_log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
