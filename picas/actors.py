# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2016, Jan Bot

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Created on Mon Jun  4 11:46:25 2012

@author: Jan Bot
"""

import sys
import time

class RunActor(object):
    """Executor class to be overwritten in the client implementation.
    """
    def __init__(self, iterator, modifier):
        """
        @param iterator: the view iterator to get the tokens from.
        """
        self.iterator = iterator
        self.client = iterator.client
        self.modifier = modifier
    
    def run(self, maxtime=-1):
        """Run method of the actor, executes the application code by iterating
        over the available tokens in CouchDB.
        """
        start = time.time()
        self.prepare_env()
        for key, ref, token in self.iterator:            
            self.prepare_run()
            self.process_token(ref, token)
            self.cleanup_run()
            if maxtime > 0:
                now = time.time()
                if now - start > maxtime:
                    sys.exit(0)
        self.cleanup_env()
        
    def prepare_env(self, *kargs, **kwargs):
        """Method to be called to prepare the environment to run the 
        application.
        """
        pass
    
    def prepare_run(self, *kargs, **kwargs):
        """Code to run before a token gets processed. Used e.g. for fetching
        inputs.
        """
        pass
    
    def process_token(self, key, token):
        """The function to overwrite which processes the tokens themselves.
        @param key: the token key. Should not be used to hold anything
        informative as it is mainly used to determine the order in which the
        tokens are returned.
        @param key: the key indicating where the token is stored in the 
        database.
        @param token: the token itself. !WARNING
        """
        modification = ()
        for k, v in token.iteritems():
            print k, v
        raise NotImplementedError
        return modification

    def cleanup_run(self, *kargs, **kwargs):
        """Code to run after a token has been processed.
        """
        pass
    
    def cleanup_env(self, *kargs, **kwargs):
        """Method which gets called after the run method has completed.
        """
        pass
    
    def unlock_all(self, view):
        rows = self.client.get_all(view)
        updated_tokens = []
        for row in rows:
            updated_tokens.append(
                    self.modifier.unlock(row['key'], row['value'])
            )
        status = self.client.update_all(updated_tokens)
        return status
