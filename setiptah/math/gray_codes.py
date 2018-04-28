"""Functions dealing with Gray codes.

Any Hamiltonian cycle on the Qn defines a Gray code.
http://mathworld.wolfram.com/HypercubeGraph.html

There are lots of Gray codes.
http://oeis.org/A091299

Code (see below) to go between Gray code index and vertex.
https://en.wikipedia.org/wiki/Gray_code

"""


def invert(b):
  return 0 if b else 1


def scalar_xor(a, b):
  # fine over {0, 1}
  return 0 if a == b else 1


def xor(v1, v2):
  f = lambda (a, b): scalar_xor(a, b)
  return tuple(map(f, zip(v1, v2)))


def right_shift(vector):
  blist = list(vector)
  result = tuple([0] + blist[:-1])
  return result


def bin_to_gray(bits):
  """Get the $n$th element of the canonical Gray code.

  Args:
    bits (tuple[{0,1}]): A binary representation of $n$.

  Returns:
    tuple[{0,1}]: The element.

  """
  return xor(bits, right_shift(bits))


def gray_to_bin(gray_bits):
  """Get the index $i$ of an element in the canonical Gray code.

  Args:
    gray_bits (tuple[{0,1}]): A Gray code element (hypercube vertex).

  Returns:
    tuple[{0,1}]: A binary representation of its index in Gray code sequence.

  """
  bits = mask = gray_bits
  while not all(b == 0 for b in mask):
    mask = right_shift(mask)
    bits = xor(bits, mask)
  return bits


def to_decimal(vector):
  return int(''.join(map(str, vector)), 2)


def to_binary(n, k):
  """Convert $n$ to binary, and crop or zero-pad to length $k$."""
  a = bin(n)[2:]
  b = a[-k:]
  c = b.zfill(k)
  return tuple(int(b) for b in c)


if __name__ == '__main__':
  ns = range(10)
  bs = map(lambda b: to_binary(b, 4), ns)
  grays = map(bin_to_gray, bs)
  bs_ = map(gray_to_bin, grays)
  ns_ = map(to_decimal, bs_)

  indices = map(to_decimal, grays)
