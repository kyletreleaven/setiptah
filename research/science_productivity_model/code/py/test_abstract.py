import unittest

from datamodel import abstract_attributes


class TestAbstractAttrs(unittest.TestCase):

  @abstract_attributes('a')
  class A(object):
    @property
    def x(self):
      return self.a

  def test_require_attrs_pass(self):

    class B(TestAbstractAttrs.A):
      a = 42

    assert B().x == 42

  def test_require_attrs_fail(self):
    # https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
    def subclass():
      class B(TestAbstractAttrs.A):
        pass

    self.assertRaises(NotImplementedError, subclass)


if __name__ == '__main__':
  unittest.main()
