from abc import ABCMeta, abstractmethod, abstractproperty


class Putter:
  __metaclass__ = ABCMeta

  @abstractmethod
  def put_text(self, string):
    assert(isinstance(string,str))

  def getcolor(self):
    raise NotImplementedError()

  def setcolor(self, value):
    assert(isinstance(string,str))

  color = abstractproperty(getcolor, setcolor)
