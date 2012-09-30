#!/usr/bin/python
from ciphers import caesar, substitution, vigenere, transposition
from cryptanalysis import caesar_brute_force, vigenere_brute_force, long_word_attack
from common.string import normalize_text
from cryptanalysis.language_stats import LanguageStats
from common.lang_model import LangModel
from common.files import get_lang_path, readfile, savefile, send_to_output
import argparse

parser = argparse.ArgumentParser(description='Cryptanalysis historical ciphers')
parser.add_argument('-i', metavar='input_file', help="Path to the input file with text")
parser.add_argument('-o', metavar='output_file', help="Path to the output file")
parser.add_argument('-e', metavar='cipher', help="Encrypt text from input file using cipher")
parser.add_argument('-d', metavar='cipher', help="Decrypt text from input file using cipher")
parser.add_argument('-k', metavar='key', help="Key for a cipher")
parser.add_argument('-t', metavar='input_text', default = "", help="Input text for the program")
parser.add_argument('-c', metavar='cipher', help="Input text will be cracked using cipher's cracking method")
parser.add_argument('--text', action="store_true", help="Program will print decrypted text instead of key")
args = parser.parse_args()

if args.i:
	input_text = readfile(args.i)
elif args.t:
	input_text = args.t
else:
	raise Exception("Input text not found")

input_text = normalize_text(input_text)

ciphers = {
	'caesar' : caesar.Caesar,
	'subs' : substitution.Substitution,
	'vig' : vigenere.Vigenere,
	'trans' : transposition.Transposition
}

crackers = {
	'caesar' : caesar_brute_force.CaesarBruteForce,
	'vig' : vigenere_brute_force.VigenereBruteForce,
	'trans' : long_word_attack.LongWordAttack
}

### Encrypting
if args.e:
	cipher = ciphers[args.e.lower()]()
	cipher_text = cipher.encrypt(input_text, args.k)
	send_to_output(cipher_text, args.o)

## Decrypting
if args.d:
	cipher = ciphers[args.d.lower()]()
	decrypted_text = cipher.decrypt(input_text, args.k)
	send_to_output(decrypted_text, args.o)

### Cracking
if args.c:
	langmodel = LangModel(get_lang_path('cs'))
	langstats = LanguageStats(langmodel)
	cracker = crackers[args.c]()
	cracked_key = cracker.crack(input_text, langstats)
	if args.text:
		cracked_text = ciphers[args.c]().decrypt(input_text, cracked_key)
		send_to_output(cracked_text, args.o)
	else:
		send_to_output(cracked_key, args.o)