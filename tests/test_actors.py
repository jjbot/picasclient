from test_mock import MockDB, MockRun
from nose.tools import assert_true, assert_equals


class TestRun():

    def _callback(self, task):
        assert_true(task.id in [t['_id'] for t in MockDB.TASKS])
        assert_true(task['lock'] > 0)
        self.count += 1

    def test_run(self):
        self.count = 0
        runner = MockRun(self._callback)
        runner.run()
        assert_equals(self.count, len(MockDB.TASKS))
