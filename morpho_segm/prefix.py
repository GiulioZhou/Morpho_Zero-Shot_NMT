# -*- coding: utf-8 -*-

from nltk.corpus import stopwords

tok_p = "##"
special = "?!\"(=:;,.\'[{"

#https://en.wiktionary.org/wiki/Category:Italian_prefixes
ita_prefix = ['epistolo', 'spermato', 'allergo', 'antropo', 'carcino',
		'cherato', 'cinesio', 'cistico', 'cortico', 'dattilo', 'dermato',
		'deutero', 'elettro', 'elminto', 'enantio', 'estesio', 'faringo',
		'farmaco', 'galatto', 'galvano', 'geronto', 'guardia', 'idrossi',
		'laringo', 'magneto', 'maxillo', 'meccano', 'meteoro', 'mirmeco',
		'oftalmo', 'parteno', 'spettro', 'stomato', 'strepto', 'talasso',
		'tossico', 'tracheo', 'adreno', 'ampelo', 'archeo', 'attino',
		'austro', 'belone', 'biblio', 'brachi', 'bronco', 'calori', 'cardio',
		'cefalo', 'centro', 'cerato', 'chemio', 'cinesi', 'circon', 'circum',
		'clepto', 'condro', 'contra', 'contro', 'cripto', 'cristo', 'critto',
		'dacrio', 'dendro', 'destro', 'dodeca', 'dolico', 'echino', 'embrio',
		'entero', 'entomo', 'eritro', 'esacis', 'franco', 'funghi', 'gastro',
		'genito', 'gineco', 'glitto', 'glosso', 'glotto', 'guarda', 'immuno',
		'ispano', 'istero', 'laparo', 'latino', 'malaco', 'megalo', 'musico',
		'onfalo', 'ornito', 'palato', 'pleuro', 'pneumo', 'proteo', 'pseudo',
		'quadri', 'quadru', 'seleno', 'sincro', 'speleo', 'stereo', 'strato',
		'tanato', 'terato', 'toraco', 'vetero', 'adeno', 'adipo', 'amilo',
		'andro', 'anemo', 'anglo', 'aorto', 'archi', 'artro', 'astro',
		'audio', 'bleno', 'calco', 'calli', 'callo', 'carbo', 'cario',
		'carpo', 'carto', 'centi', 'cheto', 'chilo', 'chiro', 'ciano',
		'ciber', 'ciclo', 'cisti', 'cisto', 'clado', 'clino', 'cloro',
		'coleo', 'colpo', 'copro', 'cosmo', 'criso', 'cromo', 'crono',
		'derma', 'dermo', 'desmo', 'diplo', 'econo', 'elaio', 'emato',
		'entro', 'epato', 'eroto', 'estra', 'etero', 'extra', 'fanta',
		'femto', 'ferri', 'ferro', 'fisio', 'flebo', 'fosfo', 'freno',
		'frigo', 'fungi', 'fuori', 'gallo', 'gastr', 'glico', 'gonio',
		'grafo', 'gravi', 'greco', 'iatro', 'icono', 'infra', 'inter',
		'intra', 'intro', 'italo', 'ittio', 'labio', 'latto', 'leuco',
		'linfo', 'lombo', 'macro', 'masto', 'medio', 'mezzo', 'micro',
		'milli', 'miria', 'molti', 'morfo', 'multi', 'narco', 'necro',
		'nefro', 'neuro', 'nevro', 'nipio', 'nitro', 'normo', 'oligo',
		'oltre', 'onico', 'osteo', 'paleo', 'palin', 'penta', 'petro',
		'picro', 'piezo', 'plani', 'pluri', 'polio', 'porno', 'porta',
		'prano', 'proto', 'pseud', 'psico', 'quadr', 'quasi', 'radio',
		'retro', 'retto', 'sapro', 'scafo', 'scato', 'scoto', 'siero',
		'simil', 'sismo', 'socio', 'sopra', 'sotto', 'sovra', 'spiro',
		'sporo', 'steno', 'stilo', 'super', 'tachi', 'tardo', 'tecno',
		'terio', 'termo', 'tetra', 'tossi', 'trans', 'tribo', 'trico',
		'ultra', 'vibro', 'video', 'xanto', 'acro', 'aden', 'aero', 'afro',
		'agio', 'agri', 'agro', 'algo', 'ambi', 'ammo', 'anfi', 'ante', 'anti',
		'anto', 'aplo', 'arci', 'areo', 'auri', 'auro', 'auto', 'avan', 'avio',
		'bari', 'baro', 'bati', 'bato', 'bene', 'brio', 'caco', 'calo', 'capo',
		'cata', 'ceno', 'cent', 'cine', 'cino', 'cito', 'crio', 'cris', 'deca',
		'deci', 'demo', 'dici', 'dopo', 'ecto', 'eleo', 'elio', 'endo', 'enna',
		'ento', 'epta', 'equi', 'ergo', 'erio', 'etno', 'etta', 'etto', 'euro',
		'ezio', 'fago', 'feno', 'fico', 'filo', 'fito', 'fono', 'foto', 'geno',
		'giga', 'gine', 'giro', 'gono', 'ideo', 'idio', 'idro', 'iero', 'igro',
		'indo', 'iper', 'ipno', 'ippo', 'ipso', 'isco', 'isto', 'kilo', 'lava',
		'lipo', 'liso', 'lito', 'logo', 'maxi', 'mega', 'meno', 'meso', 'meta',
		'mico', 'mini', 'miso', 'mono', 'moto', 'nano', 'naso', 'nord', 'noso',
		'oclo', 'ofio', 'oleo', 'olig', 'oltr', 'omeo', 'onni', 'opto', 'orto',
		'ossi', 'otta', 'para', 'pato', 'pedo', 'peri', 'piro', 'poli', 'post',
		'rino', 'rodo', 'scia', 'semi', 'silo', 'sino', 'sito', 'sopr', 'sott',
		'stra', 'tele', 'tipo', 'tomo', 'tono', 'topo', 'toss', 'tras', 'vice',
		'xeno', 'xero', 'xilo', 'zigo', 'zimo', 'alo', 'ana', 'apo', 'ben',
		'bin', 'bio', 'bis', 'cis', 'dis', 'duo', 'eco', 'ego', 'emi', 'emo',
		'eno', 'epi', 'esa', 'eso', 'eto', 'geo', 'ipo', 'iso', 'mal', 'mio',
		'neo', 'olo', 'omo', 'oro', 'oto', 'ovi', 'ovo', 'pan', 'pio', 'pre',
		'pro', 'reo', 'rin', 'sub', 'sud', 'teo', 'tio', 'tra', 'tri', 'udo',
		'uni', 'uro', 'zoo', 'bi', 'de', 'di', 'ex', 'il', 'im', 'in', 'ir',
		'oo', 're', 'ri']


# https://en.wikipedia.org/wiki/English_prefix
eng_prefix = ['counter', 'electro', 'circum', 'contra', 'contro', 'crypto',
		'deuter', 'franco', 'hetero', 'megalo', 'preter', 'pseudo', 'after',
		'under', 'amphi', 'anglo', 'astro', 'extra', 'hydro', 'hyper',
		'infra', 'inter', 'intra', 'micro', 'multi', 'multi', 'ortho',
		'paleo', 'photo', 'proto', 'quasi', 'retro', 'socio', 'super',
		'supra', 'trans', 'ultra', 'anti', 'back', 'down', 'fore', 'hind',
		'midi', 'mini', 'over', 'post', 'self', 'step', 'with', 'afro',
		'ambi', 'anti', 'arch', 'auto', 'cryo', 'demi', 'demo', 'euro',
		'gyro', 'hemi', 'homo', 'hypo', 'ideo', 'idio', 'indo', 'macr',
		'maxi', 'mega', 'meta', 'mono', 'omni', 'para', 'peri', 'pleo',
		'poly', 'post', 'pros', 'pyro', 'semi', 'tele', 'vice', 'dis',
		'mid', 'mis', 'off', 'out', 'pre', 'pro', 'twi', 'ana', 'apo',
		'bio', 'cis', 'con', 'com', 'col', 'cor', 'dia', 'dis', 'dif',
		'duo', 'eco', 'epi', 'geo', 'iso', 'mal', 'mon', 'neo', 'non',
		'pan', 'ped', 'per', 'pod', 'pre', 'pro', 'sub', 'sup', 'sur',
		'syn', 'syl', 'sym', 'tri', 'uni', 'be', 'by', 'co', 'de', 'en',
		'em', 'ex', 'on', 're', 'un', 'up', 'an', 'ap', 'bi', 'co', 'de',
		'di', 'du', 'en', 'el', 'em', 'ep', 'ex', 'in', 'im', 'ir', 'ob', 'sy']

#https://en.wiktionary.org/wiki/Category:German_prefixes
de_prefix = ['auseinander', 'schwieger', 'anthropo', 'entgegen', 'herunter',
		'zusammen', 'elektro', 'general', 'wegwerf', 'zurecht', 'achter',
		'anheim', 'binnen', 'einzel', 'gastro', 'herauf', 'heraus', 'herein',
		'hervor', 'hetero', 'hinauf', 'hinaus', 'hinein', 'hinter', 'kardio',
		'kontra', 'küchen', 'nieder', 'riesen', 'scheiß', 'sonder', 'voraus',
		'vorbei', 'vorder', 'vorher', 'wieder', 'zurück', 'after', 'aller',
		'astro', 'außen', 'balto', 'durch', 'empor', 'extra', 'gegen',
		'haupt', 'herab', 'heran', 'herum', 'hinzu', 'inter', 'intra',
		'kyber', 'meist', 'melde', 'neben', 'nicht', 'nitro', 'paläo',
		'phyto', 'porno', 'stein', 'stief', 'stock', 'unter', 'voran',
		'wider', 'afro', 'ambi', 'anti', 'auto', 'ertz', 'fort', 'hypo',
		'miss', 'myko', 'nach', 'nord', 'ober', 'onko', 'piko', 'post',
		'quer', 'raus', 'rein', 'rück', 'theo', 'thio', 'über', 'vize',
		'voll', 'zwie', 'alt', 'auf', 'aus', 'auß', 'bei', 'bey', 'bio',
		'dar', 'ein', 'emp', 'ent', 'erz', 'her', 'hin', 'miß', 'mit',
		'neo', 'neu', 'öko', 'pan', 'prä', 'sau', 'sym', 'ver', 'vor',
		'weg', 'zer', 'zur', 'ab', 'an', 'be', 'da', 'er', 'ge', 'ob',
		'um', 'un', 'ur', 'ze', 'zu']

#https://en.wiktionary.org/wiki/Category:Dutch_prefixes
nl_prefix = ['betovergroot', 'lievelings', 'mannetjes', 'overgroot',
		'vrouwtjes', 'mercapto', 'carcino', 'elektro', 'hydroxy', 'noorder',
		'spectro', 'vooruit', 'achter', 'binnen', 'buiten', 'cardio',
		'chloor', 'chromo', 'contra', 'hetero', 'kanker', 'kinesi',
		'middel', 'midden', 'ooster', 'psycho', 'strato', 'tering',
		'thermo', 'tussen', 'wester', 'zuider', 'aarts', 'aller',
		'amino', 'astro', 'bloed', 'boven', 'broom', 'centi', 'chemo',
		'cyano', 'cyclo', 'fluor', 'fysio', 'groot', 'hecto', 'homeo',
		'hoofd', 'infra', 'klote', 'kunst', 'kwasi', 'micro', 'milli',
		'multi', 'neven', 'onder', 'opeen', 'opper', 'petro', 'quasi',
		'radio', 'reuze', 'snert', 'steno', 'stief', 'super', 'tegen',
		'terug', 'trans', 'tyfus', 'voort', 'yocto', 'yotta', 'zepto',
		'zetta', 'acro', 'anti', 'atmo', 'atto', 'cyto', 'deca', 'deci',
		'door', 'filo', 'fono', 'foto', 'giga', 'hept', 'homo', 'hypo',
		'jood', 'kilo', 'mede', 'mega', 'meth', 'mono', 'nano', 'niet',
		'octo', 'over', 'pedo', 'pent', 'peri', 'peta', 'pico', 'poly',
		'post', 'prop', 'pyro', 'tele', 'tera', 'theo', 'thio', 'vice',
		'voor', 'weer', 'xylo', 'zelf', 'aan', 'apo', 'avi', 'bij', 'bio',
		'but', 'con', 'dec', 'des', 'dis', 'dys', 'eco', 'epi', 'eth', 'exa',
		'geo', 'her', 'hex', 'kei', 'kut', 'min', 'mis', 'non', 'oct', 'oer',
		'ont', 'oor', 'oud', 'pan', 'rot', 'sub', 'syn', 'toe', 'tri', 'uit',
		'ver', 'wan', 'wel', 'af', 'al', 'an', 'be', 'de', 'di', 'er', 'et',
		'ge', 'in', 'na', 'on', 'op', 'te']

#https://ro.wiktionary.org/wiki/Categorie:Prefixe_%C3%AEn_rom%C3%A2n%C4%83
ro_prefix = ['parapara', 'pluspoli', 'politico', 'portpost', 'antropo',
		'electro', 'infanti', 'balneo', 'cardio', 'câteși', 'contra',
		'ftizio', 'mecano', 'medico', 'pseudo', 'sexsex', 'simili', 'vavice',
		'aceto', 'adeno', 'audio', 'carpo', 'centi', 'cromo', 'extra',
		'ftori', 'helio', 'hidro', 'hiper', 'infra', 'inter', 'intra',
		'între', 'lacto', 'macro', 'micro', 'moldo', 'multi', 'paleo',
		'pluri', 'proto', 'radio', 'servo', 'silvo', 'super', 'supra',
		'tehno', 'termo', 'tetra', 'trans', 'ultra', 'umidi', 'video',
		'aero', 'agro', 'ante', 'anti', 'arhi', 'atot', 'auto', 'deca',
		'echi', 'filo', 'fono', 'foto', 'hexa', 'hipo', 'kilo', 'loco',
		'logo', 'mega', 'meta', 'mini', 'mono', 'moto', 'omni', 'orto',
		'peri', 'pico', 'prea', 'semi', 'stră', 'tele', 'tera', 'topo',
		'zimo', 'ana', 'bio', 'con', 'des', 'neo', 'non', 'pan', 'pre',
		'răs', 'reo', 'sub', 'tri', 'tus', 'uni', 'bi', 'ex', 'im', 'in'
		, 'în', 'ne', 're']


prefixes = {
	"italian": ita_prefix,
	"english": eng_prefix,
	"german": de_prefix,
	"dutch": nl_prefix,
	"romanian": ro_prefix
}

def prefix_segmenter(lang, word):
	punctuations = ""
	result = ""

	#Remove punctuations and return if stopword
	while word:
		if word[0] in special:
			punctuations = punctuations + word[0]
			word = word[1:]
		else:
			break
	if word.lower().rstrip(" ") in list(stopwords.words(lang)):
		return punctuations + word

	# How many iterations?
	for i in range(2):
		for prefix in prefixes[lang]:
			if word.lower().startswith(prefix) and word[:-len(prefix)] and word[len(prefix)] != " ":
				if not word.startswith(prefix): #uppercase
					prefix = prefix.title()
				result = result + " " + prefix + tok_p
				word = word[len(prefix):]
				break

	return " " + punctuations + (result + " " + word).lstrip(" ")

#
# if __name__ == "__main__":
# 	import sys
#
# 	word = sys.argv[1]
# 	print (prefix_segmenter(sys.argv[2], word))
