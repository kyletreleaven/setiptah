# Encrypted Speech

Encryption keys and ciphertexts are usually provided in formats that are slow, awkward, and error prone for transmission by spoken word.  Instead, can we code against a dictionary of English words for a more natural medium?

In other words, can we re-purpose an interesting idea to encourage device-assisted, spoken-word encryption.

[xkcd/936](https://xkcd.com/936/)

# Initial approach

Use a power-of-two part of the English dictionary

# TODO

Apply arithmetic coding for streaming radix conversion?  Solve precision issues in "range coding".

* [article](http://michael.dipperstein.com/arithmetic/)
* Cover and Thomas, Information Theory 2nd. Ed, Chapter 13, p.436

Essentially, a problem of radix conversion, e.g., from string -> hex, i.e., # in base 2^4 -> # in base |english|.

Can we combine range encoding with an arbitrary "Huffman tree"?
	* Create the prefix-free character tree of, e.g., an English dictionary.
	* Both this and a binary bit stream can be interpretted through the lens of range encoding.
	* Thus, convert a binary stream into a sequence of English words.  Word length is a reasonable proxy for entropy in natural language.


# Alternative, "residual" bases approach

Another kind of interesting alternative approach

[article](https://www.checkmyworking.com/2012/06/converting-a-stream-of-binary-digits-to-a-stream-of-base-n-digits/)
