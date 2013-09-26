#!/usr/env python

from picas.actors import RunActor
from picas.clients import CouchClient
from picas.iterators import BasicViewIterator
from picas.modifiers import BasicTokenModifier

class ExampleActor(RunActor):
    def __init__(self, iterator, modifier):
        #RunActor.__init__(iterator, modifier)
        # This is what happens in RunActor:
        self.iterator = iterator
        self.client = iterator.client
        self.modifier = modifier

        # Make a copy of the db reference
        self.db = iterator.client.db

    def prepare_env(self, *kargs, **kvargs):
        pass

    def prepare_run(self, *kargs, **kvargs):
        pass

    def process_token(self, ref, token):
        # this is where all the work gets done. Start editing here.
        
        print token
        
        token = self.modifier.close(token)
        self.db[ref[0]] = token
        aslkdfjalj


    def cleanup_run(self, *kargs, **kvargs):
        pass

    def cleanup_env(self, *kargs, **kvargs):
        pass

def main():
    client = CouchClient(url="http://localhost:5984", db='test')
    modifier = BasicTokenModifier()
    iterator = BasicViewIterator(client, "example/todo", modifier)
    actor = ExampleActor(iterator, modifier)
    actor.run()

if __name__ == '__main__':
    main()
