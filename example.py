#!/usr/env python
"""
The MIT License (MIT)

Copyright (c) 2016, Jan Bot

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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
