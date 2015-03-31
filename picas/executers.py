# -*- coding: utf-8 -*-
"""
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
