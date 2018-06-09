"""
# https://stackoverflow.com/questions/45248243/most-pythonic-way-to-declare-an-abstract-class-property

TODO(ktreleav): Patterns for ADTs.

"""

import abc
from abc import abstractmethod


def abstract_attributes(*attrs):
  """Add attribute and typed-attribute checking to a base class.

  TODO(ktreleav): Add typed_attrs.
  """

  class meta(_RequireAttributesMetaBase):
    @classmethod
    def required_attributes(cls):
      return list(attrs)

  def wrapper(cls):
    if issubclass(meta, type(cls)):
      meta_ = meta
    else:
      class meta_(meta, type(cls)):
        pass

    # https://stackoverflow.com/questions/22609272/python-typename-bases-dict
    bases_ = [_RequireAttributesMetaBase.base]
    bases_.extend(cls.__bases__)
    cls_ = meta_(cls.__name__, tuple(bases_), dict(cls.__dict__))
    return cls_

  return wrapper


class _RequireAttributesMetaBase(type, metaclass=abc.ABCMeta):
  """Base class for attribute-checking metaclasses.

  """
  @classmethod
  @abstractmethod
  def required_attributes(mcs):
    """Get a list of the attributes to check.

    """

  def __init__(cls, name, bases, attrs):
    if _RequireAttributesMetaBase.base in bases:
      return  # We don't need to super().__init__?

    meta = type(cls)  # i.e., mcs, a subclass.
    for attr in meta.required_attributes():
      if attrs.get(attr, NotImplemented) is NotImplemented:
        raise NotImplementedError('class {} must define attribute {}'
                                  .format(cls, attr))

  class base(object):
    """A "passport" class used as a direct base of abstract_attribute base classes.

    Allows child classes to pass through metaclass __init__ without attribute checks.

    """
    pass
