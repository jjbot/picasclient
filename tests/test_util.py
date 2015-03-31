from picas.util import merge_dicts, Timer
from nose.tools import assert_equal, assert_true
import time


class TestMerge():

    def setup(self):
        self.a = {'a': 1, 'b': 2}
        self.b = {'a': 2, 'c': 3}

    def test_merge_all(self):
        c = merge_dicts(self.a, self.b)
        assert_equal(c['a'], self.b['a'])
        assert_equal(self.b['a'], 2)
        assert_equal(self.a['a'], 1)
        assert_equal(len(self.a), 2)
        assert_equal(len(self.b), 2)
        assert_equal(len(c), 3)
        assert_equal(c['b'], self.a['b'])
        assert_equal(c['c'], self.b['c'])

    def test_merge_empty(self):
        c = merge_dicts(self.a, {})
        assert_equal(c, self.a)

    def test_empty_merge(self):
        c = merge_dicts({}, self.a)
        assert_equal(c, self.a)

    def test_empty_empty_merge(self):
        assert_equal(merge_dicts({}, {}), {})


def test_timer():
    timer = Timer()
    time.sleep(0.2)
    assert_true(timer.elapsed() >= 0.2)
    assert_true(timer.elapsed() < 0.4)
    timer.reset()
    assert_true(timer.elapsed() < 0.2)
