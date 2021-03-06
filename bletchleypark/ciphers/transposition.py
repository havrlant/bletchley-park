import string

class Transposition(object):
	"""Transposition cipher"""
	def __init__(self):
		super(Transposition, self).__init__()
	
	def encrypt(self, open_text, key):
		key = self._repair_key(key)
		partition = self._partition_text(open_text, len(key))
		mapping = self._get_mapping(key)
		res = [self._shuffle_letters(x, mapping) for x in partition]
		return "".join(map(lambda *x: "".join(x), *res))

	def decrypt(self, cipher_text, key):
		key = self._repair_key(key)
		partition = self._partition_text_decrypt(cipher_text, len(cipher_text) / len(key))
		reshuffled_text = "".join(partition)
		partition = self._partition_text(reshuffled_text, len(key))
		mapping = {v:k for k,v in self._get_mapping(key).items()}
		return "".join(self._shuffle_letters(x, mapping) for x in partition)

	def _repair_key(self, key):
		mapping = enumerate(sorted(enumerate(key), key=lambda x: x[1]))
		mapping = map(lambda (a, b): (chr(ord('a')+a), b[0]), mapping)
		mapping = map(lambda (a, b): a, sorted(mapping, key = lambda x: x[1]))
		return "".join(mapping)

	def _shuffle_letters(self, letters, mapping):
		return "".join(letters[mapping[i]] for i in range(len(letters)))

	def _get_mapping(self, key):
		return {ord(k)-ord('a'):ord(v)-ord('a') for k, v in zip(string.ascii_lowercase, key)}

	def _partition_text(self, text, length):
		temp = []
		for i, char in enumerate(text, 1):
			if i % length == 0:
				temp.append(char)
				yield temp
				temp = []
			else:
				temp.append(char)
		if temp:
			if len(temp) < length:
				temp += ('x' * (length - len(temp)))
				yield temp

	def _partition_text_decrypt(self, text, number):
		classes = {x:[] for x in range(number)}
		for i, char in enumerate(text):
			classes[i % number].append(char)
		return map(lambda x: "".join(x[1]), sorted(classes.items(), key=lambda x: x[0]))