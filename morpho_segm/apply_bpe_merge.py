#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Rico Sennrich

"""Use operations learned with learn_bpe.py to encode a new text.
The text will not be smaller, but use only a fixed vocabulary, with rare words
encoded as variable-length sequences of subword units.

Reference:
Rico Sennrich, Barry Haddow and Alexandra Birch (2015). Neural Machine Translation of Rare Words with Subword Units.
Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (ACL 2016). Berlin, Germany.
"""

from __future__ import unicode_literals, division

import sys
import os
import inspect
import codecs
import io
import argparse
import re
import warnings

# hack for python2/3 compatibility
from io import open
argparse.open = open

class BPE(object):

	def __init__(self, codes, merges=-1, separator='@@', vocab=None, glossaries=None):

		codes.seek(0)
		offset=1

		# check version information
		firstline = codes.readline()
		if firstline.startswith('#version:'):
			self.version = tuple([int(x) for x in re.sub(r'(\.0+)*$','', firstline.split()[-1]).split(".")])
			offset += 1
		else:
			self.version = (0, 1)
			codes.seek(0)

		self.bpe_codes = [tuple(item.strip('\r\n ').split(' ')) for (n, item) in enumerate(codes) if (n < merges or merges == -1)]

		for i, item in enumerate(self.bpe_codes):
			if len(item) != 2:
				sys.stderr.write('Error: invalid line {0} in BPE codes file: {1}\n'.format(i+offset, ' '.join(item)))
				sys.stderr.write('The line should exist of exactly two subword units, separated by whitespace\n'.format(' '.join(item)))
				sys.exit(1)

		# some hacking to deal with duplicates (only consider first instance)
		self.bpe_codes = dict([(code,i) for (i,code) in reversed(list(enumerate(self.bpe_codes)))])

		self.bpe_codes_reverse = dict([(pair[0] + pair[1], pair) for pair,i in self.bpe_codes.items()])

		self.separator = separator

		self.vocab = vocab

		self.glossaries = glossaries if glossaries else []

		self.cache = {}

	def process_line(self, line):
		"""segment line, dealing with leading and trailing whitespace"""

		out = ""

		leading_whitespace = len(line)-len(line.lstrip('\r\n '))
		if leading_whitespace:
			out += line[:leading_whitespace]

		out += self.merge(line)

		trailing_whitespace = len(line)-len(line.rstrip('\r\n '))
		if trailing_whitespace and trailing_whitespace != len(line):
			out += line[-trailing_whitespace:]

		return out

	#Merge from left to right
	def merge(self, sentence):
		output = []
		word = sentence.split()
		# print(self.bpe_codes_reverse)
		if len(sentence) <= 1:
			return ' '.join(word)

		for i in range(len(word)):
			if output:
				pair = output[-1] + word[i]
				if pair in self.bpe_codes_reverse.keys():
					output = output[:-1] #What's the complexity of .pop() ?
					output.append(pair)
				else:
					output.append(word[i])
			else:
				output.append(word[i])

		for i in range(len(output)): # Remove the special token in the middle of the words
			pref = output[i].endswith("##")
			suf = output[i].startswith("§§")
			new = output[i].replace("§§", "").replace("##", "")
			output[i] = new + "##" if pref else new
			output[i] = "§§" + output[i] if suf else output[i]

		return ' '.join(output)

	#Merge the most frequent pairs first
	def merge_freq(self, sentence):
		output = []
		word = sentence.split()
		# print(self.bpe_codes)
		if len(sentence) <= 1:
			return ' '.join(word)

		i = 0
		while i < len(word):
			# print (output)
			current = word[i]
			while True: #So basically we push on the output the output but also the possible right merge
				if output:
					if i+1 == len(word):
						merge_r = False
					else:
						pair_r = current + word[i+1]
						merge_r = pair_r in self.bpe_codes_reverse.keys()
					pair_l = output[-1] + current
					merge_l = pair_l in self.bpe_codes_reverse.keys()
					if merge_l and merge_r and tuple((output[-1],word[i])) in self.bpe_codes.keys() and tuple((word[i],word[i+1])) in self.bpe_codes.keys(): # 2 possible merge -> Check the most frequent one

						if self.bpe_codes[(tuple((word[i],word[i+1])))] < self.bpe_codes[(tuple((output[-1],word[i])))]:
							merge_l = False

					if merge_l: #There is only a merge left, or the merge left has higher frequency
						output = output[:-1] #What's the complexity of .pop() ?
						current = pair_l
					# elif merge_r:
					# 	current = pair_r
					# 	i += 1
					else: #No possible merge or we can only merge right
						output.append(current)
						break
				else:
					output.append(current)
					break

			i += 1

		return ' '.join(output)
def create_parser(subparsers=None):

	if subparsers:
		parser = subparsers.add_parser('apply-bpe',
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description="learn BPE-based word segmentation")
	else:
		parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description="learn BPE-based word segmentation")

	parser.add_argument(
		'--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
		metavar='PATH',
		help="Input file (default: standard input).")
	parser.add_argument(
		'--codes', '-c', type=argparse.FileType('r'), metavar='PATH',
		required=True,
		help="File with BPE codes (created by learn_bpe.py).")
	parser.add_argument(
		'--merges', '-m', type=int, default=-1,
		metavar='INT',
		help="Use this many BPE operations (<= number of learned symbols)"+
			 "default: Apply all the learned merge operations")
	parser.add_argument(
		'--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
		metavar='PATH',
		help="Output file (default: standard output)")
	parser.add_argument(
		'--separator', '-s', type=str, default='@@', metavar='STR',
		help="Separator between non-final subword units (default: '%(default)s'))")
	parser.add_argument(
		'--vocabulary', type=argparse.FileType('r'), default=None,
		metavar="PATH",
		help="Vocabulary file (built with get_vocab.py). If provided, this script reverts any merge operations that produce an OOV.")
	parser.add_argument(
		'--vocabulary-threshold', type=int, default=None,
		metavar="INT",
		help="Vocabulary threshold. If vocabulary is provided, any word with frequency < threshold will be treated as OOV")
	parser.add_argument(
		'--glossaries', type=str, nargs='+', default=None,
		metavar="STR",
		help="Glossaries. The strings provided in glossaries will not be affected"+
			 "by the BPE (i.e. they will neither be broken into subwords, nor concatenated with other subwords")

	return parser


def read_vocabulary(vocab_file, threshold):
	"""read vocabulary file produced by get_vocab.py, and filter according to frequency threshold.
	"""

	vocabulary = set()

	for line in vocab_file:
		word, freq = line.strip('\r\n ').split(' ')
		freq = int(freq)
		if threshold == None or freq >= threshold:
			vocabulary.add(word)

	return vocabulary

if __name__ == '__main__':

	currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	newdir = os.path.join(currentdir, 'subword_nmt')
	if os.path.isdir(newdir):
		warnings.simplefilter('default')
		warnings.warn(
			"this script's location has moved to {0}. This symbolic link will be removed in a future version. Please point to the new location, or install the package and use the command 'subword-nmt'".format(newdir),
			DeprecationWarning
		)

	# python 2/3 compatibility
	if sys.version_info < (3, 0):
		sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
		sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
		sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
	else:
		sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
		sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
		sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True, line_buffering=True)

	parser = create_parser()
	args = parser.parse_args()

	# read/write files as UTF-8
	args.codes = codecs.open(args.codes.name, encoding='utf-8')
	if args.input.name != '<stdin>':
		args.input = codecs.open(args.input.name, encoding='utf-8')
	if args.output.name != '<stdout>':
		args.output = codecs.open(args.output.name, 'w', encoding='utf-8')
	if args.vocabulary:
		args.vocabulary = codecs.open(args.vocabulary.name, encoding='utf-8')

	if args.vocabulary:
		vocabulary = read_vocabulary(args.vocabulary, args.vocabulary_threshold)
	else:
		vocabulary = None

	bpe = BPE(args.codes, args.merges, args.separator, vocabulary, args.glossaries)

	for line in args.input:
		args.output.write(bpe.process_line(line))
