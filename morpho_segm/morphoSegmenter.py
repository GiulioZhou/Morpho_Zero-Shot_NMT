#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Giulio Zhou

from suffixRemover import SuffixSegmenter
from itaSuffix import ita_segmenter
from engSuffix import eng_segmenter
from prefix import prefix_segmenter
import sys

languages = ["it","en","de","ro","nl"]


def it(i,o, lang):
	with open(i,"r") as input:
		with open(o,"a") as output:
			for line in input:
				txt = " "
				for word in line.split():
					txt += prefix_segmenter(lang, ita_segmenter(word).lstrip(" "))
				output.write(txt+"\n")

def eng(i,o, lang):
	with open(i,"r") as input:
		with open(o,"a") as output:
			for line in input:
				txt = " "
				for word in line.split():
					txt += prefix_segmenter(lang, eng_segmenter(word).lstrip(" "))
				output.write(txt+"\n")

def other(i,o,lang):
	stemmer = SuffixSegmenter(lang)
	with open(i,"r") as input:
		with open(o,"a") as output:
			for line in input:
				txt = " "
				for word in line.split():
					txt += prefix_segmenter(lang, stemmer.stem(word).lstrip(" "))
				output.write(txt+"\n")


segmenter = {
	"italian": it,
	"english": eng,
	"romanian": other,
	"german": other,
	"dutch": other
}

language = {
	"it": "italian",
	"en": "english",
	"ro": "romanian",
	"de": "german",
	"nl": "dutch"
}

if __name__ == '__main__':
	segmenter[language[sys.argv[1]]](sys.argv[2],sys.argv[3],language[sys.argv[1]])
