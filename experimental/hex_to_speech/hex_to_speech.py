"""Convert between hex encoding and Encrypted speech.

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

import math


def char_to_hex(c):
	return hex(ord(c))[-2:]

def string_to_hex(string):
	return ''.join(char_to_hex(c) for c in string)

def split_every(a_list, k):
	return [ a_list[i:i+k] for i in xrange(0,len(a_list), k) ]

def hex_to_char(char_hex):
	return chr(int(char_hex,16))

def hex_to_string(hex_string):
	hexes = split_every(hex_string,2)
	return ''.join(hex_to_char(h) for h in hexes)


def hexchar_to_bin(hex_char):
	n = int(hex_char,16)
	return bin(n)[2:].zfill(4)


def hex_to_bin(hex_string):
	return ''.join(hexchar_to_bin(h) for h in hex_string)


# TODO(ktreleav): First efficiency improvement would be have a pre-processed structure for language.

def sublang(lang):
	n = len(lang)
	k = int(math.floor(math.log(n,2)))
	return lang[:2**k], k

def hex_to_language(hex_string, language):
	bits = hex_to_bin(hex_string)

	lang = sorted(language)
	lang, p = sublang(lang)

	word_keys = [int(bs,2) for bs in split_every(bits,p)]
	return ' '.join(lang[wk] for wk in word_keys)


def language_to_hex(sentence, language):
	words = sentence.split()

	lang = sorted(language)
	lang, p = sublang(lang)

	indices = [ lang.index(w) for w in words ]

	# each index contributes p bits
	bits = ''.join(bin(i)[2:].zfill(p) for i in indices)
	bgroups = split_every(bits,4)

	return ''.join(hex(int(bs,2))[2:] for bs in bgroups)


def encrypt(plaintext, enc_key, language):

	# TODO(ktreleav): Substitute an *actual* encryption scheme
	def _base_encrypt(plaintext, enc_key):
		return string_to_hex(plaintext)

	hex_ciphertext = _base_encrypt(plaintext, enc_key)

	return hex_to_language(hex_ciphertext, language)


def decrypt(cipherspeech, dec_key, language):

	hex_ciphertext = language_to_hex(cipherspeech, language)

	# TODO(ktreleav): Substitute an *actual* decryption scheme
	def _base_decrypt(ciphertext, dec_key):
		return hex_to_string(ciphertext)

	return _base_decrypt(hex_ciphertext, dec_key)	


if __name__ == '__main__':
	import random

	if True:
		with open('wordsEn.txt','r') as f:
			LANGUAGE = list(line.strip() for line in f.readlines())
	else:
		LANGUAGE = [ c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' ]


	if False:
		# "testing"
		alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

		num_test = 10
		test_len = 20
		tests = [ ''.join(random.choice(alphabet) for _ in xrange(test_len)) for _ in xrange(num_test)]

		hexes = [ string_to_hex(t) for t in tests ]
		encs = [ hex_to_language(h, LANGUAGE) for h in hexes ]

		dechexes = [ language_to_hex(e, LANGUAGE) for e in encs ] 
		decs = [ hex_to_string(h) for h in dechexes ]

		print [ a == b for a, b in zip(tests, decs)]
