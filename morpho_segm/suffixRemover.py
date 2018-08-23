# -*- coding: utf-8 -*-

import re, nltk

from nltk import compat
from nltk.corpus import stopwords
from nltk.stem import porter
from nltk.stem.util import suffix_replace

from nltk.stem.api import StemmerI

tok_s = "§§"
special = "?!\")=:;,.\']}"


class SuffixSegmenter(StemmerI):

	"""
	Snowball Stemmer

	The following languages are supported:
	Arabic, Danish, Dutch, English, Finnish, French, German,
	Hungarian, Italian, Norwegian, Portuguese, Romanian, Russian,
	Spanish and Swedish.

	The algorithm for English is documented here:

		Porter, M. \"An algorithm for suffix stripping.\"
		Program 14.3 (1980): 130-137.

	The algorithms have been developed by Martin Porter.
	These stemmers are called Snowball, because Porter created
	a programming language with this name for creating
	new stemming algorithms. There is more information available
	at http://snowball.tartarus.org/

	The stemmer is invoked as shown below:

	>>> from nltk.stem import SnowballStemmer
	>>> print(" ".join(SnowballStemmer.languages)) # See which languages are supported
	arabic danish dutch english finnish french german hungarian
	italian norwegian porter portuguese romanian russian
	spanish swedish
	>>> stemmer = SnowballStemmer("german") # Choose a language
	>>> stemmer.stem("Autobahnen") # Stem a word
	'autobahn'

	Invoking the stemmers that way is useful if you do not know the
	language to be stemmed at runtime. Alternatively, if you already know
	the language, then you can invoke the language specific stemmer directly:

	>>> from nltk.stem.snowball import GermanStemmer
	>>> stemmer = GermanStemmer()
	>>> stemmer.stem("Autobahnen")
	'autobahn'

	:param language: The language whose subclass is instantiated.
	:type language: str or unicode
	:param ignore_stopwords: If set to True, stopwords are
							 not stemmed and returned unchanged.
							 Set to False by default.
	:type ignore_stopwords: bool
	:raise ValueError: If there is no stemmer for the specified
						   language, a ValueError is raised.
	"""

	languages = ("dutch", "english", "german", "italian", "romanian")

	def __init__(self, language, ignore_stopwords=False):
		if language not in self.languages:
			raise ValueError("The language '{0}' is not supported.".format(language))
		stemmerclass = globals()[language.capitalize() + "Stemmer"]
		self.stemmer = stemmerclass(ignore_stopwords)
		self.stem = self.stemmer.stem
		self.stopwords = self.stemmer.stopwords

	def stem(self, token):
		return self.stemmer.stem(self, token)

@compat.python_2_unicode_compatible
class _LanguageSpecificStemmer(StemmerI):

	"""
	This helper subclass offers the possibility
	to invoke a specific stemmer directly.
	This is useful if you already know the language to be stemmed at runtime.

	Create an instance of the Snowball stemmer.

	:param ignore_stopwords: If set to True, stopwords are
							 not stemmed and returned unchanged.
							 Set to False by default.
	:type ignore_stopwords: bool
	"""

	def __init__(self, ignore_stopwords=False):
		# The language is the name of the class, minus the final "Stemmer".
		language = type(self).__name__.lower()
		if language.endswith("stemmer"):
			language = language[:-7]

		self.stopwords = set()
		if ignore_stopwords:
			try:
				for word in stopwords.words(language):
					self.stopwords.add(word)
			except IOError:
				raise ValueError("{!r} has no list of stopwords. Please set"
								 " 'ignore_stopwords' to 'False'.".format(self))

	def __repr__(self):
		"""
		Print out the string representation of the respective class.

		"""
		return "<{0}>".format(type(self).__name__)

class PorterStemmer(_LanguageSpecificStemmer, porter.PorterStemmer):
	"""
	A word stemmer based on the original Porter stemming algorithm.

		Porter, M. \"An algorithm for suffix stripping.\"
		Program 14.3 (1980): 130-137.

	A few minor modifications have been made to Porter's basic
	algorithm.  See the source code of the module
	nltk.stem.porter for more information.

	"""
	def __init__(self, ignore_stopwords=False):
		_LanguageSpecificStemmer.__init__(self, ignore_stopwords)
		porter.PorterStemmer.__init__(self)

class _StandardStemmer(_LanguageSpecificStemmer):

	"""
	This subclass encapsulates two methods for defining the standard versions
	of the string regions R1, R2, and RV.

	"""

	def _r1r2_standard(self, word, vowels):
		"""
		Return the standard interpretations of the string regions R1 and R2.

		R1 is the region after the first non-vowel following a vowel,
		or is the null region at the end of the word if there is no
		such non-vowel.

		R2 is the region after the first non-vowel following a vowel
		in R1, or is the null region at the end of the word if there
		is no such non-vowel.

		:param word: The word whose regions R1 and R2 are determined.
		:type word: str or unicode
		:param vowels: The vowels of the respective language that are
					   used to determine the regions R1 and R2.
		:type vowels: unicode
		:return: (r1,r2), the regions R1 and R2 for the respective word.
		:rtype: tuple
		:note: This helper method is invoked by the respective stem method of
			   the subclasses DutchStemmer, FinnishStemmer,
			   FrenchStemmer, GermanStemmer, ItalianStemmer,
			   PortugueseStemmer, RomanianStemmer, and SpanishStemmer.
			   It is not to be invoked directly!
		:note: A detailed description of how to define R1 and R2
			   can be found at http://snowball.tartarus.org/texts/r1r2.html

		"""
		r1 = ""
		r2 = ""
		for i in range(1, len(word)):
			if word[i] not in vowels and word[i-1] in vowels:
				r1 = word[i+1:]
				break

		for i in range(1, len(r1)):
			if r1[i] not in vowels and r1[i-1] in vowels:
				r2 = r1[i+1:]
				break

		return (r1, r2)



	def _rv_standard(self, word, vowels):
		"""
		Return the standard interpretation of the string region RV.

		If the second letter is a consonant, RV is the region after the
		next following vowel. If the first two letters are vowels, RV is
		the region after the next following consonant. Otherwise, RV is
		the region after the third letter.

		:param word: The word whose region RV is determined.
		:type word: str or unicode
		:param vowels: The vowels of the respective language that are
					   used to determine the region RV.
		:type vowels: unicode
		:return: the region RV for the respective word.
		:rtype: unicode
		:note: This helper method is invoked by the respective stem method of
			   the subclasses ItalianStemmer, PortugueseStemmer,
			   RomanianStemmer, and SpanishStemmer. It is not to be
			   invoked directly!

		"""
		rv = ""
		if len(word) >= 2:
			if word[1] not in vowels:
				for i in range(2, len(word)):
					if word[i] in vowels:
						rv = word[i+1:]
						break

			elif word[0] in vowels and word[1] in vowels:
				for i in range(2, len(word)):
					if word[i] not in vowels:
						rv = word[i+1:]
						break
			else:
				rv = word[3:]

		return rv

class DutchStemmer(_StandardStemmer):

	"""
	The Dutch Snowball stemmer.

	:cvar __vowels: The Dutch vowels.
	:type __vowels: unicode
	:cvar __step1_suffixes: Suffixes to be deleted in step 1 of the algorithm.
	:type __step1_suffixes: tuple
	:cvar __step3b_suffixes: Suffixes to be deleted in step 3b of the algorithm.
	:type __step3b_suffixes: tuple
	:note: A detailed description of the Dutch
		   stemming algorithm can be found under
		   http://snowball.tartarus.org/algorithms/dutch/stemmer.html

	"""

	__vowels = "aeiouy\xE8"
	__step1_suffixes = ("heden", "ene", "en", "se", "s")
	__step3b_suffixes = ("baar", "lijk", "bar", "end", "ing", "ig")

	def stem(self, word):
		"""
		Stem a Dutch word and return the stemmed form.

		:param word: The word that is stemmed.
		:type word: str or unicode
		:return: The stemmed form.
		:rtype: unicode

		"""
		punctuations = ""
		result = ""
		while word:
			if word[-1] in special:
				punctuations = word[-1] + punctuations
				word = word[:-1]
			else:
				break

		heden = False
		# word = word.lower()

		if word.lower() in list(stopwords.words('dutch')):
			return word + " " + punctuations + " "

		step2_success = False

		# Vowel accents are removed.
		# word = (word.replace("\xE4", "a").replace("\xE1", "a")
					# .replace("\xEB", "e").replace("\xE9", "e")
					# .replace("\xED", "i").replace("\xEF", "i")
					# .replace("\xF6", "o").replace("\xF3", "o")
					# .replace("\xFC", "u").replace("\xFA", "u"))

		# An initial 'y', a 'y' after a vowel,
		# and an 'i' between self.__vowels is put into upper case.
		# As from now these are treated as consonants.
		if word.startswith("y"):
			word = "".join(("Y", word[1:]))

		for i in range(1, len(word)):
			if word[i-1] in self.__vowels and word[i] == "y":
				word = "".join((word[:i], "Y", word[i+1:]))

		for i in range(1, len(word)-1):
			if (word[i-1] in self.__vowels and word[i] == "i" and
			   word[i+1] in self.__vowels):
				word = "".join((word[:i], "I", word[i+1:]))

		r1, r2 = self._r1r2_standard(word, self.__vowels)

		# R1 is adjusted so that the region before it
		# contains at least 3 letters.
		for i in range(1, len(word)):
			if word[i] not in self.__vowels and word[i-1] in self.__vowels:
				if len(word[:i+1]) < 3 and len(word[:i+1]) > 0:
					r1 = word[3:]
				elif len(word[:i+1]) == 0:
					return word + " " + punctuations + " "
				break

		# STEP 1
		for suffix in self.__step1_suffixes:
			if r1.endswith(suffix):
				if suffix == "heden":
					word = suffix_replace(word, suffix, "heid")
					r1 = suffix_replace(r1, suffix, "heid")
					heden = True
					if r2.endswith("heden"):
						r2 = suffix_replace(r2, suffix, "heid")

				elif (suffix in ("ene", "en") and
					  not word.endswith("heden") and
					  word[-len(suffix)-1] not in self.__vowels and
					  word[-len(suffix)-3:-len(suffix)] != "gem"):
					result =  tok_s + suffix + " " + result
					word = word[:-len(suffix)]
					r1 = r1[:-len(suffix)]
					r2 = r2[:-len(suffix)]
					if word.endswith(("kk", "dd", "tt")):
						result =  tok_s + word[-1] + " " + result
						word = word[:-1]
						r1 = r1[:-1]
						r2 = r2[:-1]

				elif (suffix in ("se", "s") and
					  word[-len(suffix)-1] not in self.__vowels and
					  word[-len(suffix)-1] != "j"):
					result =  tok_s + suffix + " " + result
					word = word[:-len(suffix)]
					r1 = r1[:-len(suffix)]
					r2 = r2[:-len(suffix)]
				break

		# STEP 2
		if r1.endswith("e") and word[-2] not in self.__vowels:
			step2_success = True
			result =  tok_s + word[-1] + " " + result
			word = word[:-1]
			r1 = r1[:-1]
			r2 = r2[:-1]

			if word.endswith(("kk", "dd", "tt")):
				result =  tok_s + word[-1] + " " + result
				word = word[:-1]
				r1 = r1[:-1]
				r2 = r2[:-1]

		# STEP 3a
		if r2.endswith("heid") and word[-5] != "c":
			if heden :
				result =  tok_s + "heden " + result
			else:
				result =  tok_s + "heid " + result
			word = word[:-4]
			r1 = r1[:-4]
			r2 = r2[:-4]

			if (r1.endswith("en") and word[-3] not in self.__vowels and
				word[-5:-2] != "gem"):
				result =  tok_s + "en " + result
				word = word[:-2]
				r1 = r1[:-2]
				r2 = r2[:-2]

				if word.endswith(("kk", "dd", "tt")):
					result =  tok_s + word[-1] + " " + result
					word = word[:-1]
					r1 = r1[:-1]
					r2 = r2[:-1]

		# STEP 3b: Derivational suffixes
		for suffix in self.__step3b_suffixes:
			if r2.endswith(suffix):
				if suffix in ("end", "ing"):
					result =  tok_s + suffix + " " + result
					word = word[:-3]
					r2 = r2[:-3]

					if r2.endswith("ig") and word[-3] != "e":
						result =  tok_s + suffix + " " + result
						word = word[:-2]
					else:
						if word.endswith(("kk", "dd", "tt")):
							result =  tok_s + word[-1] + " " + result
							word = word[:-1]

				elif suffix == "ig" and word[-3] != "e":
					result =  tok_s + suffix + " " + result
					word = word[:-2]

				elif suffix == "lijk":
					result =  tok_s + suffix + " " + result
					word = word[:-4]
					r1 = r1[:-4]

					if r1.endswith("e") and word[-2] not in self.__vowels:
						result =  tok_s + word[-1] + " " + result
						word = word[:-1]
						if word.endswith(("kk", "dd", "tt")):
							result =  tok_s + word[-1] + " " + result
							word = word[:-1]

				elif suffix == "baar":
					result =  tok_s + suffix + " " + result
					word = word[:-4]

				elif suffix == "bar" and step2_success:
					result =  tok_s + suffix + " " + result
					word = word[:-3]
				break

		# # STEP 4: Undouble vowel
		# if len(word) >= 4:
		#     if word[-1] not in self.__vowels and word[-1] != "I":
		#         if word[-3:-1] in ("aa", "ee", "oo", "uu"):
		#             if word[-4] not in self.__vowels:
		#                 word = "".join((word[:-3], word[-3], word[-1]))

		# All occurrences of 'I' and 'Y' are put back into lower case.
		word = word.replace("I", "i").replace("Y", "y")


		return (word + " " + result).rstrip(" ")+ " " + punctuations + " "


class GermanStemmer(_StandardStemmer):

	"""
	The German Snowball stemmer.

	:cvar __vowels: The German vowels.
	:type __vowels: unicode
	:cvar __s_ending: Letters that may directly appear before a word final 's'.
	:type __s_ending: unicode
	:cvar __st_ending: Letter that may directly appear before a word final 'st'.
	:type __st_ending: unicode
	:cvar __step1_suffixes: Suffixes to be deleted in step 1 of the algorithm.
	:type __step1_suffixes: tuple
	:cvar __step2_suffixes: Suffixes to be deleted in step 2 of the algorithm.
	:type __step2_suffixes: tuple
	:cvar __step3_suffixes: Suffixes to be deleted in step 3 of the algorithm.
	:type __step3_suffixes: tuple
	:note: A detailed description of the German
		   stemming algorithm can be found under
		   http://snowball.tartarus.org/algorithms/german/stemmer.html

	"""

	__vowels = "aeiouy\xE4\xF6\xFC"
	__s_ending = "bdfghklmnrt"
	__st_ending = "bdfghklmnt"

	__step1_suffixes = ("ern", "em", "er", "en", "es", "e", "s")
	__step2_suffixes = ("est", "en", "er", "st")
	__step3_suffixes = ("isch", "lich", "heit", "keit",
						  "end", "ung", "ig", "ik")

	def stem(self, word):
		"""
		Stem a German word and return the stemmed form.

		:param word: The word that is stemmed.
		:type word: str or unicode
		:return: The stemmed form.
		:rtype: unicode

		"""
		# word = word.lower()
		punctuations = ""
		result = ""
		while word:
			if word[-1] in special:
				punctuations = word[-1] + punctuations
				word = word[:-1]
			else:
				break
		if word.lower() in list(stopwords.words('german')):
			return word + " " + punctuations + " "

		# word = word.replace("\xDF", "ss")

		# Every occurrence of 'u' and 'y'
		# between vowels is put into upper case.
		for i in range(1, len(word)-1):
			if word[i-1] in self.__vowels and word[i+1] in self.__vowels:
				if word[i] == "u":
					word = "".join((word[:i], "U", word[i+1:]))

				elif word[i] == "y":
					word = "".join((word[:i], "Y", word[i+1:]))

		r1, r2 = self._r1r2_standard(word, self.__vowels)

		# R1 is adjusted so that the region before it
		# contains at least 3 letters.
		for i in range(1, len(word)):
			if word[i] not in self.__vowels and word[i-1] in self.__vowels:
				if len(word[:i+1]) < 3 and len(word[:i+1]) > 0:
					r1 = word[3:]
				elif len(word[:i+1]) == 0:
					return word + " " + punctuations + " "
				break

		# STEP 1
		for suffix in self.__step1_suffixes:
			if r1.endswith(suffix):
				if (suffix in ("en", "es", "e") and
					word[-len(suffix)-4:-len(suffix)] == "niss"):
					result =   tok_s + "s " + tok_s + suffix + " " + result
					word = word[:-len(suffix)-1]
					r1 = r1[:-len(suffix)-1]
					r2 = r2[:-len(suffix)-1]

				elif suffix == "s":
					if word[-2] in self.__s_ending:
						result =  tok_s + word[-1] + " " + result
						word = word[:-1]
						r1 = r1[:-1]
						r2 = r2[:-1]
				else:
					result =  tok_s + suffix + " " + result
					word = word[:-len(suffix)]
					r1 = r1[:-len(suffix)]
					r2 = r2[:-len(suffix)]
				break

		# STEP 2
		for suffix in self.__step2_suffixes:
			if r1.endswith(suffix):
				if suffix == "st":
					if word[-3] in self.__st_ending and len(word[:-3]) >= 3:
						result =  tok_s + word[-2:] + " " + result
						word = word[:-2]
						r1 = r1[:-2]
						r2 = r2[:-2]
				else:
					result =  tok_s + suffix + " " + result
					word = word[:-len(suffix)]
					r1 = r1[:-len(suffix)]
					r2 = r2[:-len(suffix)]
				break

		# STEP 3: Derivational suffixes
		for suffix in self.__step3_suffixes:
			if r2.endswith(suffix):
				if suffix in ("end", "ung"):
					if ("ig" in r2[-len(suffix)-2:-len(suffix)] and
						"e" not in r2[-len(suffix)-3:-len(suffix)-2]):
						result =   tok_s + word[-len(suffix)-2:-len(suffix)] + " " + tok_s + suffix + " " + result
						word = word[:-len(suffix)-2]
					else:
						result =  tok_s + suffix + " " + result
						word = word[:-len(suffix)]

				elif (suffix in ("ig", "ik", "isch") and
					  "e" not in r2[-len(suffix)-1:-len(suffix)]):
					result =  tok_s + suffix + " " + result
					word = word[:-len(suffix)]

				elif suffix in ("lich", "heit"):
					if ("er" in r1[-len(suffix)-2:-len(suffix)] or
						"en" in r1[-len(suffix)-2:-len(suffix)]):
						result =   tok_s + word[-len(suffix)-2:-len(suffix)] + " " + tok_s + suffix + " " + result
						word = word[:-len(suffix)-2]
					else:
						result =  tok_s + suffix + " " + result
						word = word[:-len(suffix)]

				elif suffix == "keit":
					if "lich" in r2[-len(suffix)-4:-len(suffix)]:
						result =   tok_s + word[-len(suffix)-4:-len(suffix)] + " " + tok_s + suffix + " " + result
						word = word[:-len(suffix)-4]

					elif "ig" in r2[-len(suffix)-2:-len(suffix)]:
						result =   tok_s + word[-len(suffix)-2:-len(suffix)] + " " + tok_s + suffix + " " + result
						word = word[:-len(suffix)-2]
					else:
						result =  tok_s + suffix + " " + result
						word = word[:-len(suffix)]
				break

		# Umlaut accents are removed and
		# 'u' and 'y' are put back into lower case.
		word = (word.replace("\xE4", "a").replace("\xF6", "o")
					.replace("\xFC", "u").replace("U", "u")
					.replace("Y", "y"))


		return (word + " " + result).rstrip(" ") + " " + punctuations + " "

class RomanianStemmer(_StandardStemmer):

	"""
	The Romanian Snowball stemmer.

	:cvar __vowels: The Romanian vowels.
	:type __vowels: unicode
	:cvar __step0_suffixes: Suffixes to be deleted in step 0 of the algorithm.
	:type __step0_suffixes: tuple
	:cvar __step1_suffixes: Suffixes to be deleted in step 1 of the algorithm.
	:type __step1_suffixes: tuple
	:cvar __step2_suffixes: Suffixes to be deleted in step 2 of the algorithm.
	:type __step2_suffixes: tuple
	:cvar __step3_suffixes: Suffixes to be deleted in step 3 of the algorithm.
	:type __step3_suffixes: tuple
	:note: A detailed description of the Romanian
		   stemming algorithm can be found under
		   http://snowball.tartarus.org/algorithms/romanian/stemmer.html

	"""

	__vowels = "aeiou\u0103\xE2\xEE"
	__step0_suffixes = ('iilor', 'ului', 'elor', 'iile', 'ilor',
						'atei', 'a\u0163ie', 'a\u0163ia', 'aua',
						'ele', 'iua', 'iei', 'ile', 'ul', 'ea',
						'ii')
	__step1_suffixes = ('abilitate', 'abilitati', 'abilit\u0103\u0163i',
						'ibilitate', 'abilit\u0103i', 'ivitate',
						'ivitati', 'ivit\u0103\u0163i', 'icitate',
						'icitati', 'icit\u0103\u0163i', 'icatori',
						'ivit\u0103i', 'icit\u0103i', 'icator',
						'a\u0163iune', 'atoare', '\u0103toare',
						'i\u0163iune', 'itoare', 'iciva', 'icive',
						'icivi', 'iciv\u0103', 'icala', 'icale',
						'icali', 'ical\u0103', 'ativa', 'ative',
						'ativi', 'ativ\u0103', 'atori', '\u0103tori',
						'itiva', 'itive', 'itivi', 'itiv\u0103',
						'itori', 'iciv', 'ical', 'ativ', 'ator',
						'\u0103tor', 'itiv', 'itor')
	__step2_suffixes = ('abila', 'abile', 'abili', 'abil\u0103',
						'ibila', 'ibile', 'ibili', 'ibil\u0103',
						'atori', 'itate', 'itati', 'it\u0103\u0163i',
						'abil', 'ibil', 'oasa', 'oas\u0103', 'oase',
						'anta', 'ante', 'anti', 'ant\u0103', 'ator',
						'it\u0103i', 'iune', 'iuni', 'isme', 'ista',
						'iste', 'isti', 'ist\u0103', 'i\u015Fti',
						'ata', 'at\u0103', 'ati', 'ate', 'uta',
						'ut\u0103', 'uti', 'ute', 'ita', 'it\u0103',
						'iti', 'ite', 'ica', 'ice', 'ici', 'ic\u0103',
						'osi', 'o\u015Fi', 'ant', 'iva', 'ive', 'ivi',
						'iv\u0103', 'ism', 'ist', 'at', 'ut', 'it',
						'ic', 'os', 'iv')
	__step3_suffixes = ('seser\u0103\u0163i', 'aser\u0103\u0163i',
						'iser\u0103\u0163i', '\xE2ser\u0103\u0163i',
						'user\u0103\u0163i', 'seser\u0103m',
						'aser\u0103m', 'iser\u0103m', '\xE2ser\u0103m',
						'user\u0103m', 'ser\u0103\u0163i', 'sese\u015Fi',
						'seser\u0103', 'easc\u0103', 'ar\u0103\u0163i',
						'ur\u0103\u0163i', 'ir\u0103\u0163i',
						'\xE2r\u0103\u0163i', 'ase\u015Fi',
						'aser\u0103', 'ise\u015Fi', 'iser\u0103',
						'\xe2se\u015Fi', '\xE2ser\u0103',
						'use\u015Fi', 'user\u0103', 'ser\u0103m',
						'sesem', 'indu', '\xE2ndu', 'eaz\u0103',
						'e\u015Fti', 'e\u015Fte', '\u0103\u015Fti',
						'\u0103\u015Fte', 'ea\u0163i', 'ia\u0163i',
						'ar\u0103m', 'ur\u0103m', 'ir\u0103m',
						'\xE2r\u0103m', 'asem', 'isem',
						'\xE2sem', 'usem', 'se\u015Fi', 'ser\u0103',
						'sese', 'are', 'ere', 'ire', '\xE2re',
						'ind', '\xE2nd', 'eze', 'ezi', 'esc',
						'\u0103sc', 'eam', 'eai', 'eau', 'iam',
						'iai', 'iau', 'a\u015Fi', 'ar\u0103',
						'u\u015Fi', 'ur\u0103', 'i\u015Fi', 'ir\u0103',
						'\xE2\u015Fi', '\xe2r\u0103', 'ase',
						'ise', '\xE2se', 'use', 'a\u0163i',
						'e\u0163i', 'i\u0163i', '\xe2\u0163i', 'sei',
						'ez', 'am', 'ai', 'au', 'ea', 'ia', 'ui',
						'\xE2i', '\u0103m', 'em', 'im', '\xE2m',
						'se')

	def stem(self, word):
		"""
		Stem a Romanian word and return the stemmed form.

		:param word: The word that is stemmed.
		:type word: str or unicode
		:return: The stemmed form.
		:rtype: unicode

		"""
		# word = word.lower()
		# nltk.download('stopwords')
		# print (self.__step0_suffixes)
		# print (self.__step1_suffixes)
		# print (self.__step2_suffixes)
		# print (self.__step3_suffixes)

		punctuations = ""
		result = ""
		while word:
			if word[-1] in special:
				punctuations = word[-1] + punctuations
				word = word[:-1]
			else:
				break

		if word.lower() in list(stopwords.words('romanian')):
			return word + " " + punctuations + " "

		step1_success = False
		step2_success = False

		for i in range(1, len(word)-1):
			if word[i-1] in self.__vowels and word[i+1] in self.__vowels:
				if word[i] == "u":
					word = "".join((word[:i], "U", word[i+1:]))

				elif word[i] == "i":
					word = "".join((word[:i], "I", word[i+1:]))

		r1, r2 = self._r1r2_standard(word, self.__vowels)
		rv = self._rv_standard(word, self.__vowels)

		# STEP 0: Removal of plurals and other simplifications
		for suffix in self.__step0_suffixes:
			if word.endswith(suffix):
				if suffix in r1:
					if suffix in ("ul", "ului"):
						result =  tok_s + suffix + " " + result
						word = word[:-len(suffix)]

						if suffix in rv:
							rv = rv[:-len(suffix)]
						else:
							rv = ""

					elif (suffix == "aua" or suffix == "atei" or
						  (suffix == "ile" and word[-5:-3] != "ab")):
						result =  tok_s + suffix[-2:] + " " + result
						word = word[:-2]

					elif suffix in ("ea", "ele", "elor"):
						result =  tok_s + suffix[1:] + " " + result
						word = word[:-len(suffix)+1]

						if suffix in rv:
							rv = suffix_replace(rv, suffix, "e")
						else:
							rv = ""

					elif suffix in ("ii", "iua", "iei",
									"iile", "iilor", "ilor"):
						result =  tok_s + suffix[1:] + " " + result
						word = word[:-len(suffix)+1]

						if suffix in rv:
							rv = suffix_replace(rv, suffix, "i")
						else:
							rv = ""

					elif suffix in ("a\u0163ie", "a\u0163ia"):
						result =  tok_s + suffix + " " + result
						word = word[:-len(suffix)+1]
				break

		# STEP 1: Reduction of combining suffixes
		while True:

			replacement_done = False

			for suffix in self.__step1_suffixes:
				if word.endswith(suffix):
					if suffix in r1:
						step1_success = True
						replacement_done = True

						if suffix in ("abilitate", "abilitati",
									  "abilit\u0103i",
									  "abilit\u0103\u0163i"):
							result =  tok_s + suffix[4:] + " " + result
							word = word[:-len(suffix)+4]

						elif suffix == "ibilitate":
							result =  tok_s + suffix[4:] + " " + result
							word = word[:-len(suffix)+4]

						elif suffix in ("ivitate", "ivitati",
										"ivit\u0103i",
										"ivit\u0103\u0163i"):
							result =  tok_s + suffix[2:] + " " + result
							word = word[:-len(suffix)+2]

						elif suffix in ("icitate", "icitati", "icit\u0103i",
										"icit\u0103\u0163i", "icator",
										"icatori", "iciv", "iciva",
										"icive", "icivi", "iciv\u0103",
										"ical", "icala", "icale", "icali",
										"ical\u0103"):
							result =  tok_s + suffix[2:] + " " + result
							word = word[:-len(suffix)+2]

						elif suffix in ("ativ", "ativa", "ative", "ativi",
										"ativ\u0103", "a\u0163iune",
										"atoare", "ator", "atori",
										"\u0103toare",
										"\u0103tor", "\u0103tori"):
							result =  tok_s + suffix[2:] + " " + result
							word = word[:-len(suffix)+2]

							if suffix in r2:
								r2 = suffix_replace(r2, suffix, "at")

						elif suffix in ("itiv", "itiva", "itive", "itivi",
										"itiv\u0103", "i\u0163iune",
										"itoare", "itor", "itori"):
							result =  tok_s + suffix[2:] + " " + result
							word = word[:-len(suffix)+2]

							if suffix in r2:
								r2 = suffix_replace(r2, suffix, "it")
					else:
						step1_success = False
					break

			if not replacement_done:
				break

		# STEP 2: Removal of standard suffixes
		for suffix in self.__step2_suffixes:
			if word.endswith(suffix):
				if suffix in r2:
					step2_success = True

					# if suffix in ("iune", "iuni"):
					#     if word[-5] == "\u0163":
					#         word = "".join((word[:-5], "t"))

					if suffix in ("ism", "isme", "ist", "ista", "iste",
									"isti", "ist\u0103", "i\u015Fti"):
						result =  tok_s + suffix[3:] + " " + result
						word = word[:-len(suffix)+3]

					else:
						result =  tok_s + suffix + " " + result
						word = word[:-len(suffix)]
				break

		# STEP 3: Removal of verb suffixes
		if not step1_success and not step2_success:
			for suffix in self.__step3_suffixes:
				if word.endswith(suffix):
					if suffix in rv:
						if suffix in ('seser\u0103\u0163i', 'seser\u0103m',
									  'ser\u0103\u0163i', 'sese\u015Fi',
									  'seser\u0103', 'ser\u0103m', 'sesem',
									  'se\u015Fi', 'ser\u0103', 'sese',
									  'a\u0163i', 'e\u0163i', 'i\u0163i',
									  '\xE2\u0163i', 'sei', '\u0103m',
									  'em', 'im', '\xE2m', 'se'):
							result =  tok_s + suffix + " " + result
							word = word[:-len(suffix)]
							rv = rv[:-len(suffix)]
						else:
							if (not rv.startswith(suffix) and
								rv[rv.index(suffix)-1] not in
								"aeio\u0103\xE2\xEE"):
								result =  tok_s + suffix + " " + result
								word = word[:-len(suffix)]
						break

		# STEP 4: Removal of final vowel
		for suffix in ("ie", "a", "e", "i", "\u0103"):
			if word.endswith(suffix):
				if suffix in rv:
					result =  tok_s + suffix + " " + result
					word = word[:-len(suffix)]
				break

		word = word.replace("I", "i").replace("U", "u")


		return (word + " " + result).rstrip(" ") + " " + punctuations + " "

#
# if __name__ == "__main__":
#     import sys
#
#     stemmer = SuffixSegmenter("dutch")
#     for word in ["opgroeiende"]:
#     #for word in "e ora la presentazione , la aggiorno ogni volta che la mostro , aggiungo nuove immagini , perché ogni volta che la mostro apprendo cose nuove .".split():
#         print (stemmer.stem(word))
