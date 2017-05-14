from collections import defaultdict
import tensorflow as tf

class VarGroup:
  def __init__(self):
    self._subgroups = defaultdict(VarGroup)
    self._vars = set()

  def get_or_create_subgroup(self, group_name):
    return self._subgroups[group_name]

  def add(self, variable):
    self._vars.add(variable)

  def get_vars(self):
    return set(self._vars)

  def get_all_vars(self):
    res = set(self._vars)
    for g in self._subgroups.itervalues():
      res.update(g.get_all_vars())
    return res

  def groups(self):
    return self._subgroups.keys()

  def get_group(self, group_key):
    return self._subgroups.get(group_key)
    
  def itergroups(self):
    return self._subgroups.iteritems()


def group_variables(var_list):
  root = VarGroup()

  for var in var_list:
    term = root
    
    varpath = var.name.split('/')[:-1]
    for arc in varpath:
      term = term.get_or_create_subgroup(arc)
    
    term.add(var)

  return root


def get_grouped_trainable_variables():
  var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
  return group_variables(var_list)


if __name__ == '__main__':
  g = VarGroup()
  g.add(0)

  A = g.get_or_create_subgroup('A')
  A.add(1)
  A.add(2)

  B = A.get_or_create_subgroup('B')
  B.add(3)
