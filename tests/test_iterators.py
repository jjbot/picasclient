from picas.iterators import TaskViewIterator
from test_mock import MockDB
from nose.tools import assert_equals, assert_true


def test_iterator():
    db = MockDB()
    for task in TaskViewIterator(db, 'view'):
        assert_true(task['lock'] > 0)
        assert_equals(task.rev, 'something')
        assert_equals(db.saved[task.id], task.value)
        break  # process one task only

    assert_equals(len(db.saved), 1)
