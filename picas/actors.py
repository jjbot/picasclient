# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 11:46:25 2012

@author: Jan Bot, Joris Borgdorff
"""
from .util import Timer
from .iterators import TaskViewIterator


class RunActor(object):

    """Executor class to be overwritten in the client implementation.
    """

    def __init__(self, db):
        """
        @param database: the database to get the tasks from.
        """
        if db is None:
            raise ValueError("Database must be initialized")

        self.db = db
        self.tasks_processed = 0

    def run(self, maxtime=None, avg_time_factor=0.0):
        """Run method of the actor, executes the application code by iterating
        over the available tasks in CouchDB.
        """
        time = Timer()
        self.prepare_env()
        try:
            for task in TaskViewIterator('todo', database=self.db):
                self.prepare_run()

                try:
                    self.process_task(task)
                except Exception as ex:
                    msg = ("Exception {0} occurred during processing: {1}"
                           .format(type(ex), ex))
                    task.error(msg, exception=ex)
                    print(msg)

                self.db.save(task)
                self.cleanup_run()
                self.tasks_processed += 1

                if maxtime is not None:
                    will_elapse = ((avg_time_factor + self.tasks_processed) *
                                   time.elapsed() / self.tasks_processed)
                    if will_elapse > maxtime:
                        break
        finally:
            self.cleanup_env()

    def prepare_env(self, *kargs, **kwargs):
        """Method to be called to prepare the environment to run the
        application.
        """
        pass

    def prepare_run(self, *kargs, **kwargs):
        """Code to run before a task gets processed. Used e.g. for fetching
        inputs.
        """
        pass

    def process_task(self, task):
        """The function to overwrite which processes the tasks themselves.
        @param key: the task key. Should not be used to hold anything
        informative as it is mainly used to determine the order in which the
        tasks are returned.
        @param key: the key indicating where the task is stored in the
        database.
        @param task: the task itself.
        """
        raise NotImplementedError

    def cleanup_run(self, *kargs, **kwargs):
        """Code to run after a task has been processed.
        """
        pass

    def cleanup_env(self, *kargs, **kwargs):
        """Method which gets called after the run method has completed.
        """
        pass

