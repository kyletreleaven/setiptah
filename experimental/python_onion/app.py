import getting
import putting


class MyGetter(getting.Getter):
  def get_text(self):
    return 'Hello World!'


class MyPutter(putting.Putter):

  def __init__(self, color=None):
    self._color = color

  def put_text(self, string):
    print ('<p><font color="%s">%s</font></p>'
      % (self.color, string))

  #@property
  def color(self):
    return self._color

  #@color.setter
  def set_color(self, value):
    assert(isinstance(value, str))
    self._color = value


def main(getter, putter):
  assert(isinstance(getter,getting.Getter))
  assert(isinstance(putter,putting.Putter))

  string = getter.get_text()
  #putter.color = 'green'
  putter.put_text(string)


if __name__ == '__main__':

  main(MyGetter(),MyPutter())
