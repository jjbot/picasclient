import socket
from .util import merge_dicts, seconds
import mimetypes
import base64
import traceback
from uuid import uuid4

''' @author Joris Borgdorff '''


class Document(object):

    ''' A CouchDB document '''

    def __init__(self, data={}, base={}):
        if isinstance(data, Document):
            data = data.value

        # Data is not from the database
        if '_rev' not in data:
            data = merge_dicts(base, data)

        self.doc = data

    def __getitem__(self, idx):
        return self.doc.__getitem__(idx)

    def __setitem__(self, idx, value):
        return self.doc.__setitem__(idx, value)

    @property
    def id(self):
        try:
            return self.doc['_id']
        except KeyError:
            raise AttributeError("_id for document is not set")

    @property
    def rev(self):
        try:
            return self.doc['_rev']
        except KeyError:
            raise AttributeError("_rev is not available: document is not "
                                 "retrieved from database")

    @id.setter
    def id(self, new_id):
        self.doc['_id'] = new_id

    @property
    def value(self):
        return self.doc

    def update(self, values):
        """Add the output of the RunActor to the task.
        """
        self.doc.update(values)

    def put_attachment(self, name, data, mimetype=None):
        if '_attachments' not in self.doc:
            self.doc['_attachments'] = {}

        if mimetype is None:
            mimetype, encoding = mimetypes.guess_type(name)
            if mimetype is None:
                mimetype = 'text/plain'

        b64data = base64.b64encode(data)
        self.doc['_attachments'][name] = {
            'content_type': mimetype, 'data': b64data}

    def get_attachment(self, name):
        ''' Gets an attachment dict from the document.
        Attachment data may not have been copied over from the
        database, in that case it will have an md5 checksum. '''
        # Copy all attributes except data, it may be very large
        attachment = {}
        for key in self.doc['_attachments'][name]:
            if key != 'data':
                attachment[key] = self.doc['_attachments'][name][key]

        if 'data' in self.doc['_attachments'][name]:
            attachment['data'] = base64.b64decode(
                self.doc['_attachments'][name]['data'])

        return attachment

    def remove_attachment(self, name):
        del self.doc['_attachments'][name]
        return self

    def _update_hostname(self):
        self.doc['hostname'] = socket.gethostname()
        return self


class Task(Document):
    __BASE = {
        'type': 'task',
        'lock': 0,
        'done': 0,
        'hostname': '',
        'scrub_count': 0,
        'input': {},
        'output': {},
        'error': []
    }

    """Class to manage task modifications with.
    """

    def __init__(self, task={}):
        super(Task, self).__init__(task, Task.__BASE)
        if '_id' not in self.doc:
            self.doc['_id'] = 'task_' + uuid4().hex

    def lock(self):
        """Function which modifies the task such that it is locked.
        """
        self.doc['lock'] = seconds()
        return self._update_hostname()

    def done(self):
        """Function which modifies the task such that it is closed for ever
        to the view that has supplied it.
        """
        self.doc['done'] = seconds()
        return self

    @property
    def input(self):
        """ Get input """
        return self.doc['input']

    @input.setter
    def input(self, value):
        """ Set input """
        self.doc['input'] = value

    @property
    def output(self):
        """Get the output from the RunActor."""
        return self.doc['output']

    @output.setter
    def output(self, output):
        """Add the input for the RunActor to the task.
        """
        self.doc['output'] = output

    def scrub(self):
        """
        Task scrubber: makes sure a task can be handed out again if it was
        locked more than t seconds ago.
        """
        if 'scrub_count' not in self.doc:
            self.doc['scrub_count'] = 0
        self.doc['scrub_count'] += 1
        self.doc['done'] = 0
        self.doc['lock'] = 0
        return self._update_hostname()

    def error(self, msg=None, exception=None):
        error = {'time': seconds()}
        if msg is not None:
            error['message'] = str(msg)

        if exception is not None:
            error['exception'] = traceback.format_exc()

        self.doc['lock'] = -1
        self.doc['done'] = -1
        if 'error' not in self.doc:
            self.doc['error'] = []
        self.doc['error'].append(error)
        return self

    def has_error(self):
        return self.doc['lock'] == -1

    def get_errors(self):
        try:
            return self.doc['error']
        except:
            return []


class Job(Document):
    __BASE = {
        'type': 'job',
        'hostname': '',
        'start': 0,
        'done': 0,
        'queue': 0,
        'method': '',
        'archive': 0
    }

    def __init__(self, job):
        super(Job, self).__init__(job, Job.__BASE)
        if '_id' not in self.doc:
            raise ValueError('Job ID must be set')

    def queue(self, method, host=None):
        self.doc['method'] = method
        if host is not None:
            self.doc['hostname'] = host
        self.doc['queue'] = seconds()
        return self

    def start(self):
        self.doc['start'] = seconds()
        return self._update_hostname()

    def finish(self):
        self.doc['done'] = seconds()
        return self

    def archive(self):
        if self.doc['done'] <= 0:
            self.doc['done'] = seconds()
        self.doc['archive'] = seconds()
        self.id = 'archived-' + self.id + '-' + str(seconds())
        del self.doc['_rev']
        return self
