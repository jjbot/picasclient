# -*- coding: utf-8 -*-
"""
Created on Mon May 21 16:13:58 2012

@author: Jan Bot
"""

class TokenGenerator(object):
    def __init__(self):
        pass

    @staticmethod
    def get_empty_token():
        token = {
                'input': {},
                'output': {},
                'lock': 0,
                'done': 0,
                'hostname': '',
                'scrub_count': 0,
                'type': 'token'
        }
        return token