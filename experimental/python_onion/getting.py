from abc import ABCMeta, abstractmethod


class Getter:
  __metaclass__ = ABCMeta

  @abstractmethod
  def get_text(self):
    raise NotImplementedError()
