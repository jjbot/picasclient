# -*- coding: utf-8 -*-
"""
Created on Sun May 20 18:16:41 2012

@author: Jan Bot, Leiden University & Delft University of Technology
"""

# Python imports
import threading
import logging
import Queue
from os import path

# PiCaS imports
import picasclient
from picasclient.executers import execute, execute_old


def download(remotefile, local_dir):
    picasclient.logging.debug("Downloading: " + remotefile)
    pass

def upload(localfile, srm_dir):
    picasclient.logging.debug("Uploading: " + localfile)
    pass

def download_many(files, poolsize=10):
    q = Queue.Queue()
    for k, v in files.iteritems():
        q.put(v)
    
    thread_pool = []
    for i in range(poolsize):
        d = Downloader(q)
        d.start()
        thread_pool.append(d)
    
    q.join()
    for d in thread_pool:
        d.join(1)
        
def upload_many(files, poolsize=10):
    pass
    
    
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
                picasclient.logger.error("Download of " + f + 
                        " failed after multiple tries.")
                raise EnvironmentError("Download failed.")
            self.q.task_done()


class SRMClient(object):
    def __init__(self, logger, host="srm://srm.grid.sara.nl/"):
        self.logger = logger
        self.srm_host = host

    def remote_exists(self, loc):
        """Check if a file exists on the remote location.
        @param loc: complete path on the SRM to the file.
        """
        sURL = self.srm_host + loc
        cmd = ['srmls', sURL]
        print " ".join(cmd)
        (returncode, stdout, stderr) = execute(cmd)
        if returncode == 0:
            bn = path.basename(loc)
            lines = stdout.split("\n")
            for line in lines:
                if bn in line:
                    return True
            return False
        else:
            return False
        
    def upload(self, local_file, srm_dir, check=False):
        """Upload local file to the SRM.
        @local_file: the file that needs to be copied.
        @param srm_dir: location on the SRM where the file needs to be copied
        to.
        @param check: whether to check if the local and remote files exist. 
        Default: True
        @return: location of the file on the SRM.
        """
        srm_file = path.join(srm_dir, path.basename(local_file))
        srm_url = self.srm_host + srm_file
        if check:
            if not path.isfile(local_file):
                raise EnvironmentError(10, "File not found.", local_file)
            if self.remote_exists(srm_file):
                raise EnvironmentError(11, "File exists on srm.", 
                        srm_url)
        
        cmd = ['srmcp', '-2', '-server_mode=passive', 
               'file:///' + local_file, srm_url]
        print cmd
        (returncode, stdout, stderr) = execute(cmd)
        if returncode == 0:
            pass
        else:
            raise EnvironmentError("Upload failed.")
        return srm_url
        
    def download(self, srm_file, local_dir="./", check=False):
        """Download a file from the SRM.
        @param srm_file: complete path to the file on the SRM.
        @param local_dir: directory where the file needs to be copied to.
        @return: location of the downloaded file.
        """
        local_file = path.join(local_dir, path.basename(srm_file))
        srm_url = self.srm_host + srm_file
        if check:
            if not self.remote_exists(srm_file):
                raise EnvironmentError(10, "File not found.", srm_url)
        
        cmd = ['srmcp', '-2', '-server_mode=passive', 
               srm_url, 'file:///' + local_file]
        picasclient.logger.info("Downloading: " + local_file)
        returncode = execute_old(" ".join(cmd))
        picasclient.logger.debug("Done downloading " + local_file)
        if returncode == 0:
            pass
        else:
            picasclient.logger.error("Download failed of: " + srm_file)
            raise EnvironmentError("Download failed.")
        return local_file