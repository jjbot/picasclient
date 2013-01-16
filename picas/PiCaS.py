# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 15:27:13 2012

@author: Jan Bot, Leiden University & Delft University of Technology
"""

# Import Python modules
import logging
import random
import socket
from subprocess import Popen, PIPE
import time
from os import path, system

# Import third party Python modules
import couchdb
from couchdb import Server, ResourceConflict

# Import own Python modules


# Set version for compatibility checking.
version = 0.25



            








class RemoteFile(object):
    def __init__(self):
        pass

    def check_file(self):
        pass
        # run md5hash, adler?
    
    @staticmethod
    def get_empty_file():
        f = {
            '_id': '',
            'adler32': '',
            'md5': '',
            'name': '',
            'description': '',
            'storage': {},
            'type': 'file',
        }
        return f


def main():
    """The main function, all crap goes here."""
    client = CouchClient()
    modifier = TokenModifier()
    iterator = ViewIterator(client, "test/test", modifier)
    actor = RunActor(iterator)
    actor.run()


if __name__ == '__main__':
    main()
