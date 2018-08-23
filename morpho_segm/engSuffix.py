# -*- coding: utf-8 -*-


stop = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
		"you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
		'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
		'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
		'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
		'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
		'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
		'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
		'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
		'with', 'about', 'against', 'between', 'into', 'through', 'during',
		'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
		'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
		'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
		'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
		'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
		'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',
		'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
		 "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
		 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
		 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
		 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
		 "won't", 'wouldn', "wouldn't"]


#ance/ence, ity/ty, sion/tion/xion
suffixes = ['hood', 'ment', 'ness', 'ship', 'ion', 'less',
		'age', 'nce', 'dom', 'ism', 'ist', 'est', 'ble',
		'ese', 'ful', 'ish', 'ian', 'ive', 'ous', 'ure', 'ag', 'al',
		'ee', 'er', 'or', 'ty', 'ry', 'at', 'en', 'ic',
		'iv', 'ly', 'i', 'y']


verbs = ["ate","en","ify","ise","ize", "ent"]

advs = ["ly", "wards", "ward", "wise"]

vowels = ["a","e","i","o","u","y"]

special_words = {"skis" : "ski",
				   "skies" : "sk",
				#    "dying" : "die",
				#   "lying" : "lie",
				#    "tying" : "tie",
				   "idly" : "idl",
				   "gently" : "gentl",
				#    "ugly" : "ugli",
				#    "early" : "earli",
				#    "only" : "onli",
				   "singly" : "singl",
				   "sky" : "sky",
				   "news" : "news",
				   "howe" : "howe",
				   "atlas" : "atlas",
				   "cosmos" : "cosmos",
				   "bias" : "bias",
				   "andes" : "andes",
				   "inning" : "inning",
				   "innings" : "inning",
				   "outing" : "outing",
				   "outings" : "outing",
				   "canning" : "canning",
				   "cannings" : "canning",
				   "herring" : "herring",
				   "herrings" : "herring",
				   "earring" : "earring",
				   "earrings" : "earring",
				   "proceed" : "proceed",
				   "proceeds" : "proceed",
				   "proceeded" : "proceed",
				   "proceeding" : "proceed",
				   "exceed" : "exceed",
				   "exceeds" : "exceed",
				   "exceeded" : "exceed",
				   "exceeding" : "exceed",
				   "succeed" : "succeed",
				   "succeeds" : "succeed",
				   "succeeded" : "succeed",
				   "succeeding" : "succeed"}
tok_s = "§§"

special = "?!\")=:;,.\']}"

def eng_segmenter(word):

	punctuations = ""
	result = ""
	while word:
		if word[-1] in special:
			punctuations = word[-1] + punctuations
			word = word[:-1]
		else:
			break

	if word.lower() in stop or len(word) <= 3:
		return word + " " + punctuations + " "

	elif word in special_words:
		if len(word) == len(special_words[word]):
			return special_words[word] + " " + punctuations + " "
		else:
			return (special_words[word] + " " + tok_s + word[len(special_words[word])-1:]).rstrip(" ") + " " + punctuations + " "

	for adverb in advs:
		 if word.endswith(adverb):
			 if word[:-len(adverb)]:
				 result =  tok_s + adverb + " " + result
				 word = word[:-len(adverb)]
			 break

	restart = True
	mod = False

	for verb in verbs:
		if len(word)<=3:
			return (word + " " + result).rstrip(" ") + " " + punctuations + " "
		if word.endswith(verb):
			if verb == "ent" and word.endswith("ment"): #skip if it ends with ment
				continue
			if word[:-len(verb)]:
				result =  tok_s + verb + " " + result
				word = word[:-len(verb)]
			break

	if len(word)<=3:
		return (word + " " + result).rstrip(" ") + " " + punctuations + " "

	if word[-1] == "s":
		if not word.endswith("ss") and not word.endswith("us") and not word.endswith("is") and not word.endswith("os"): #NOTE need to add more cases here
			result = tok_s + word[-1] + " " + result
			word = word[:-1]
			if word[-1] == "e":
				result = tok_s + word[-1] + " " + result
				word = word[:-1]
				if word[-1] == "i":
					result = tok_s + word[-1] + " " + result
					word = word[:-1]

	while restart:
		if len(word)<=3:
			break
		for nom in suffixes:
			if word.endswith(nom):
				if not word[:-len(nom)]:
					break
				result = tok_s + nom + " " + result
				word = word[:-len(nom)]
				mod = True
				#ance/ence, ity/ty, sion/tion/xion
				if nom == "nce" or (nom == "ty" and word[-1] == "i") or nom == "ion":
					result = tok_s + word[-1] + " " + result
					word = word[:-1]

				if nom == "ble" or (nom == "al" and word[-1] == "i"): #remove i or a before 'ble' or for 'ial'
					result = tok_s + word[-1] + " " + result
					word = word[:-1]

		try:
			for i in range (2):
				if (word[-1] in vowels) or (word[-1] == word[-2]):
					result = tok_s + word[-1] + " " + result
					word = word[:-1]
		except:
			break

		if mod:
			#remove extra vowels and doubles
			mod = False
		else:
			restart = False


	if word.endswith("ed"):
		result = tok_s + "ed " + result
		word = word[:-2]

	if word.endswith("ing"):
		result = tok_s + "ing " + result
		word = word[:-3]

	try:
		if (word[-1] in vowels) or (word[-1] == word[-2]):
			result = tok_s + word[-1] + " " + result
			word = word[:-1]
	except:
		True

	result = (word + " " + result).rstrip(" ") + " " + punctuations + " "
	return result



#
# import sys
#
# for word in sys.argv:
# 	print (eng_segmenter(word))
