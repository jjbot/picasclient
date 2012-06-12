# -*- coding: utf-8 -*-
"""
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
    def __init__(self, url, db):
        logging.Handler.__init__(self)
        self.server = Server(url=url)
        self.db = self.server[db]
        self.hostname = socket.gethostname()
        random.seed(time.time())
        self.trace_nr = int(random.random() * 100000)
    
    def emit(self, record):
        log_dict = {
            'lvl': record.levelno,
            'msg': record.msg,
            'created': record.created,
            'func': record.funcName,
            'host': self.hostname,
            'trance_nr': self.trace_nr,
            'type': 'log'
        }
        id = self.hostname + ":" + str(int(time.time())) 
        
        count = 0
        done = False
        while(count < 10 and not done):
            try:
                self.db[id] = log_dict
                done = True
            except:
                count += 1

default_log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)