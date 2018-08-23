# -*- coding: utf-8 -*-



stopwords = ['aveva', 'io', 'eravamo', 'facessi', 'avessimo', 'quante',
		'tra', 'anche', 'foste', 'ebbi', 'facesti', 'avevate', 'sullo',
		'avrebbe', 'voi', 'avevi', 'ebbe', 'siamo', 'sarei', 'stette',
		'mio', 'lei', 'chi', 'fosti', 'starai', 'facendo', 'saresti',
		'quanti', 'questi', 'sul', 'abbiamo', 'nei', 'stia', 'una', 'nella',
		'avrete', 'starei', 'faceva', 'tuoi', 'erano', 'sue', 'vostri', 'fui',
		'nostri', 'staremo', 'avessi', 'quella', 'faranno', 'starò', 'dei',
		'fanno', 'suoi', 'degli', 'avuta', 'li', 'loro', 'l', 'avendo',
		'sarebbero', 'facevamo', 'farà', 'sarete', 'mia', 'sulla', 'stiano',
		'ebbero', 'starebbero', 'quelli', 'tutti', 'nelle', 'allo', 'i',
		'stiamo', 'facevano', 'stavate', 'nostra', 'ed', 'c', 'avremmo',
		'di', 'abbiate', 'sono', 'ero', 'facemmo', 'staranno', 'stava',
		'in', 'dalle', 'hai', 'lo', 'avute', 'dagl', 'nell', 'suo', 'stai',
		'stesti', 'tu', 'che', 'sugl', 'negli', 'tuo', 'stavo', 'vostre', 'su',
		'hanno', 'fossimo', 'fosse', 'stavano', 'al', 'dallo', 'stetti', 'ma',
		'sia', 'fossi', 'vostro', 'o', 'sarà', 'dov', 'a', 'questo', 'fece',
		'saremo', 'faceste', 'facciamo', 'da', 'avrò', 'facevate', 'fu', 'ad',
		'perché', 'sareste', 'siate', 'tua', 'stavi', 'dai', 'starebbe', 'farò',
		'avresti', 'faremo', 'nostre', 'farai', 'essendo', 'stanno', 'tue',
		'stessero', 'degl', 'avesse', 'avremo', 'quanto', 'ci', 'all', 'sei',
		'se', 'avuto', 'fecero', 'dagli', 'agl', 'lui', 'quale', 'ti',
		'facessimo', 'dall', 'stessi', 'avete', 'facciano', 'nel', 'più',
		'miei', 'mi', 'farebbero', 'abbiano', 'contro', 'feci', 'agli', 'noi',
		'il', 'avesti', 'sta', 'avevano', 'stando', 'steste', 'faccia', 'cui',
		'avemmo', 'furono', 'stesse', 'sua', 'staremmo', 'dell', 'nostro',
		 'farete', 'col', 'starà', 'avrai', 'stessimo', 'sui', 'la', 'questa',
		 'avranno', 'fareste', 'stettero', 'fai', 'stemmo', 'per', 'faresti',
		 'alla', 'farei', 'dove', 'facessero', 'dello', 'staresti', 'sarò',
		 'le', 'avevo', 'gli', 'ne', 'non', 'stiate', 'ho', 'avreste',
		 'facesse', 'dal', 'nello', 'saremmo', 'starete', 'fummo', 'della',
		 'sarebbe', 'avessero', 'eravate', 'quanta', 'sarai', 'sto', 'delle',
		 'facevi', 'facevo', 'sugli', 'saranno', 'ai', 'fossero', 'eri', 'sulle',
		 'era', 'un', 'aveste', 'quello', 'mie', 'siete', 'faremmo', 'del',
		 'avevamo', 'siano', 'ha', 'quelle', 'con', 'come', 'avuti', 'è',
		 'faccio', 'farebbe', 'stavamo', 'alle', 'dalla', 'avrebbero', 'avrà',
		 'negl', 'si', 'e', 'uno', 'avrei', 'vi', 'stareste', 'abbia', 'sull',
		 'coi', 'tutto', 'facciate', 'vostra', 'queste', 'si', 'no']

general = ['icciol', 'aggin', 'tteri', 'ambul', 'issim', 'acci',
		'aggi', 'agli', 'legi', 'ment', 'tter', 'ucci', 'ucol',
		'zion', 'evol', 'frag', 'tori', 'acc', 'agg', 'agl',
		'anz', 'asc', 'azz', 'enz', 'eri', 'esc', 'età', 'ett',
		'ezz', 'fer', 'ier', 'iol', 'ism', 'ist', 'ità', 'oid',
		'ott', 'tur', 'ucc', 'uzz', 'ari', 'bil', 'fug',
		'vag', 'tiv', 'tor', 'ai', 'am', 'an', 'at', 'er', 'es',
		'in', 'on', 'os', 'ot', 'um', 'ut', 'al', 'ar',
		'ic', 'a']

suffixoids = ['archi', 'cines', 'crazi', 'grafi', 'gramm',
		'machi', 'manzi', 'potam', 'scopi', 'arch', 'crat',
		'cron', 'derm', 'drom', 'fagi', 'fagh', 'fili', 'fobi',
		'foni', 'goni', 'graf', 'iatr', 'logi', 'mach', 'mani',
		'manz', 'metr', 'morf', 'opol', 'scop', 'tomi', 'trop',
		'tter', 'urgi', 'urgh', 'cer', 'cid', 'eli', 'fag',
		'fil', 'fob', 'fon', 'fon', 'gon', 'lit', 'log', 'man',
		'tec', 'tom', 'urg', 'urg', 'vor', 'el']

pronouns = ['gliela', 'gliele', 'glieli', 'glielo',
		'gliene', 'sene', 'mela', 'mele', 'meli',
		'melo', 'mene', 'tela', 'tele', 'teli',
		'telo', 'tene', 'cela', 'cele', 'celi',
		'celo', 'cene', 'vela', 'vele', 'veli',
		'velo', 'vene', 'gli', 'ci', 'la', 'le',
		'li', 'lo', 'mi', 'ne', 'si', 'ti', 'vi']

#There should be "a" and "i" as well but it gives problem with other words
#that end whit these combinations, eg. 'amici' which should be devided in
#'amic i' but with "i" here it will become 'am i ci'
pron_verb = ['ar', 'er', 'ir', 'ando', 'endo',
		'iamo', 'ate', 'ete', 'ite']

conjugations = ['erebbero', 'irebbero', 'eranno', 'iranno', 'eresti',
		 'erebbe', 'eremmo', 'ereste', 'iresti', 'irebbe', 'iremmo',
		  'ireste', 'essimo', 'essero', 'issimo', 'issero', 'assimo',
		  'assero', 'avamo', 'avate', 'avano', 'evamo', 'evate',
		  'evano', 'ivamo', 'ivate', 'ivano', 'arono', 'irono',
		  'eremo', 'erete', 'iremo', 'irete', 'iamo', 'asti',
		  'ammo', 'aste', 'esti', 'emmo', 'este', 'sero', 'isti',
		  'immo', 'iste', 'erai', 'irai', 'erei', 'irei', 'iate',
		  'essi', 'esse', 'issi', 'isse', 'assi', 'asse', 'ante',
		  'ando', 'endo', 'ente', 'ete', 'ono', 'avo', 'avi', 'ava',
		  'evo', 'evi', 'eva', 'ivo', 'ivi', 'iva', 'erà', 'erò',
		  'irò', 'irà', 'ano', 'ire', 'ito', 'ino', 'are', 'ato',
		  'uto', 'ere', 'ai', 'si', 'se', 'ii', 'ir', 'ar', 'er', 'ì', 'ò',
		  'o', 'i', 'e', 'a']

noun_to_verb = ['ific', 'izz', 'eggi']

tok_s = "§§"

vowels = ["a","e","i","o","u"]

special = "?!\")=:;,.\']}"


def ita_segmenter(word):
	punctuations = ""
	while word:
		if word[-1] in special:
			punctuations = word[-1] + punctuations
			word = word[:-1]
		else:
			break

	if word.lower() in stopwords:
		return word + " " + punctuations + " "
	result = ""
	pronoun = False
	verb = False

	#The adverb suffix goes always at the very end
	for adverb in ["mente"]: #theoretically "oni" should be in this list but I have decided to remove it
		 if word.endswith(adverb):
			 if word[:-len(adverb)]:
				 result =  tok_s + adverb + " " + result
				 word = word[:-len(adverb)]
				 if word[-1] == "a":
					 result =  tok_s + "a " + result
					 word = word[:-1]
			 break

	#Check if it ends with a pronoun
	#BUG -> "parla" -> "p ar la". However, "d ar la" is a corret segmentation
	for pron in pronouns:
		if word.endswith(pron):
			if word[:-len(pron)]: #There are words like "gli" which are not suffix (although they have the same meaning, we shouldn't add the suffix token)

				#Check if is an imperative, gerund or infinitive verb (otherwise we don't remove the pronoun)
				#The reason is because there are words that end with the same sillables but have not that suffix!
				for conj in pron_verb:
					if word[:-len(pron)].endswith(conj):
						if word[:-len(pron)-len(conj)]: #I don't know there is any word like this, but it can be
							word = word[:-len(pron)-len(conj)]
							pronoun = True
							verb = True
							if len(pron) > 3: #For compound suffixes such as "gliela", "glieli", "mena" etc... The second suffix is always 2 characters length
									result = tok_s + conj + " " + tok_s + pron[:len(pron)-2] + " " + tok_s + pron[len(pron)-2:] + " " + result
							else:
									result = tok_s + conj + " " + tok_s + pron + " " + result
							break

	if not pronoun:
		#Check if it's a verb
		for conj in conjugations:
			if word.endswith(conj):
				if word[:len(conj)]:
					word = word[:-len(conj)]
					if conj in ['are', 'ere', 'ire']: #I separate the e because it can be dropped sometimes
						conj = conj[:-1] + " " + tok_s + "e"
					verb = True
					result = tok_s + conj + " " + result
				break

	if verb:
		#Tecnically every noun can be transformed into a verb, and a noun can have suffixes
		#However it is really rare to have a suffixed word transformed to a verb
		#E.g. conoscenza can be transformed into conoscenzeggiarlo
		for suffix in noun_to_verb:
			if word.endswith(suffix):
				return (word[:-len(suffix)]  + " " + tok_s + suffix + " " + result).rstrip(" ") + " " + punctuations + " "

		# if conj not in vowels:
		# 	return jsonify({'result': word + " " + result})

	#I know it's repeated code and it's not really goodlooking but I didn't realy want to think about another way to do this
	try:
		#Remove vowels and h+vowel
		if word[-1] in vowels:
			for suffix in suffixoids: #check suffixoids before removing the vowels
				if word.endswith(suffix):
					if word[:-len(suffix)]:
						return (word[:-len(suffix)]  + " " + tok_s + suffix + " " + result).rstrip(" ") + " " + punctuations + " "
					break

			if word[:-1]:
				result = tok_s + word[-1] + " " + result
				word = word[:-1]
			if word[-1] == "h":
				if word[:-1]:
					result =  tok_s + "h " + result
					word = word[:-1]
	except:
		return (word + " " + result).rstrip(" ") + " " + punctuations + " "


	for suffix in suffixoids:
		if word.endswith(suffix):
			if word[:-len(suffix)]:
				return (word[:-len(suffix)]  + " " + tok_s + suffix + " " + result).rstrip(" ") + " " + punctuations + " "
		break

	restart = True
	mod = False

	for i in range(1): #How many iterations? Do till it split?
		for suffix in general:
			if word.endswith(suffix):
				if word[:-len(suffix)]:
					result = tok_s + suffix + " " + result
					word = word[:-len(suffix)]
					mod = True
				break

		if mod:
			mod = False
		else:
			restart = False

	try:
		#Remove vowels and h+vowel
		if word[-1] in vowels:
			for suffix in suffixoids: #check suffixoids before removing the vowels
				if word.endswith(suffix):
					if word[:-len(suffix)]:
						return (word[:-len(suffix)]  + " " + tok_s + suffix + " " + result).rstrip(" ") + " " + punctuations + " "
					break

			if word[:-1]:
				result = tok_s + word[-1] + " " + result
				word = word[:-1]
			if word[-1] == "h":
				if word[:-1]:
					result =  tok_s + "h " + result
					word = word[:-1]
	except:
		return (word + " " + result).rstrip(" ") + " " + punctuations + " "


	# for suffix in suffixoids: #Are they necessary?
	# 	if word.endswith(suffix):
	# 		if word[:-len(suffix)]:
	# 			result = tok_s + suffix + " " + result
	# 			word = word[:-len(suffix)]
	# 		break

	return (word + " " + result).rstrip(" ") + " " + punctuations + " "
#
#
# if __name__ == "__main__":
# 	import sys
#
# 	word = sys.argv[1]
# 	print (ita_segmenter(word))
