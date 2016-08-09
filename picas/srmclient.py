# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2016, Jan Bot

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Created on Thu May 17 15:00:59 2012

@author: Jan Bot
"""
from __future__ import print_function

import threading
import logging
import Queue

from PiCaS import SRMClient


def download(files, threads=10):
    q = Queue.Queue()
    for k, v in files.iteritems():
        q.put(v)

    thread_pool = []
    for i in range(threads):
        d = Downloader(q)
        d.start()
        thread_pool.append(d)

    q.join()
    print("Download work done, joining threads")
    for d in thread_pool:
        print("Joining: %s" % str(d.ident))
        d.join(1)


class Downloader(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.q = queue
        self.logger = logging.getLogger('Pindel')
        self.srm = SRMClient(self.logger)
        self.daemon = False

    def run(self):
        while not self.q.empty():
            f = self.q.get()
            count = 0
            done = False
            while(count < 10 and not done):
                try:
                    self.srm.download(f)
                    done = True
                except:
                    count += 1
            if(count > 9):
                raise EnvironmentError("Download failed.")
            self.q.task_done()
        print("Exiting while loop, thread should close itself...")