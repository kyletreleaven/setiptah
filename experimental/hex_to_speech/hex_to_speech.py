"""Encrypted speech.

Encryption keys and ciphertexts are usually provided in formats that are slow, awkward, and error prone for transmission by spoken word.
Instead, can we code against a dictionary of English words for a more natural medium?

In other words, can we re-purpose an interesting idea to encourage device-assisted, spoken-word encryption.

https://xkcd.com/936/
"""


# TODO(ktreleav): Apply arithmetic coding for streaming radix conversion?  Solve precision issues in "range coding".

# http://michael.dipperstein.com/arithmetic/
# Cover, Thomas, Information Theory, 2nd. Ed, Chapter 13, p.436

# Essentially, a problem of radix conversion.
# from string -> hex, i.e., # in base 2^4 -> # in base |english|
def convert(number, base1, base2):
	pass

def char_to_hex():
	return hex(ord(c))	# perhaps slice [-2:]


# Another kind of interesting alternative approach:
# https://www.checkmyworking.com/2012/06/converting-a-stream-of-binary-digits-to-a-stream-of-base-n-digits/

class BaseStream:
	def __init__(self, source_base, target_base):
		self._source_base = source_base
		self._target_base = target_base

	def push(self, n):
		pass

	def ready(self):
		pass

	def next(self):
		pass

def residuals_base(curr_base, target_base):
	# k = smallest k' s.t. curr_base^{k'} >= target_base
	# next_base = 2^k - target_base
	pass


if __name__ == '__main__':
  pass
  