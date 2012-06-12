# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 11:46:25 2012

@author: Jan Bot
"""

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
    
    def run(self):
        """Run method of the actor, executes the application code by iterating
        over the available tokens in CouchDB.
        """
        self.prepare_env()
        for key, token in self.iterator:
            self.prepare_run()
            self.process_token(key, token)
            self.cleanup_run
        self.cleanup_env()
        
    def prepare_env(self, *kargs, **kwargs):
        """Method to be called to prepare the environment to run the 
        application.
        """
        raise NotImplementedError
    
    def prepare_run(self, *kargs, **kwargs):
        """Code to run before a token gets processed. Used e.g. for fetching
        inputs.
        """
        raise NotImplementedError
    
    def process_token(self, key, token):
        modification = ()
        for k, v in token.iteritems():
            print k, v
        raise NotImplementedError
        return modification

    def cleanup_run(self, *kargs, **kwargs):
        """Code to run after a token has been processed.
        """
        raise NotImplementedError
    
    def cleanup_env(self, *kargs, **kwargs):
        """Method which gets called after the run method has completed.
        """
        raise NotImplementedError
    
    def unlock_all(self, view):
        rows = self.client.get_all(view)
        updated_tokens = []
        for row in rows:
            updated_tokens.append(
                    self.modifier.unlock(row['key'], row['value'])
            )
        status = self.client.update_all(updated_tokens)
        return status