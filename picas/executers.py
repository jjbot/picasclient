# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2016, Jan Bot

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Created on Tue Jun  5 14:02:36 2012

@author: Jan Bot
Module to easily execute commandline applications.
"""

# Python imports
from subprocess import Popen, PIPE
from os import system


def execute(args, shell=False):
    """Helper function to more easily execute applications.
    @param args: the arguments as they need to be specified for Popen.
    @return: a tuple containing the exitcode, stdout & stderr
    """
    proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=shell)
    (stdout, stderr) = proc.communicate()
    return (proc.returncode, stdout, stderr)


def execute_old(cmd):
    """Helper functino to execute an external application.
    @param cmd: the command to be executed.
    @return the exit code of the executed program.
    """
    return system(cmd)
