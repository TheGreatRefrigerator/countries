###
# Author: Amandus Butzer (amandusbutzer@gmx.de)
###

import json, os, sys, codecs, operator
from collections import OrderedDict

cwd = os.getcwd()

file = cwd + '/countries.json'
res = cwd + '/result.json'
cur = cwd + '/current countries'

with open(file, 'r') as f:
	# print f.read()
	Data = json.loads(f.read())
	Data2 = []
	for obj in Data:
		# concats names from name.native[x].common
		def nativenames(only=False):
			name = ""
			thing = obj['name']['native']
			for key in thing:
				native_common = thing[key]['common']
				common_name = obj['name']['common']
				name += native_common if name == "" else ", " + native_common if native_common not in name else ""
				name += common_name if name == "" else ", " + common_name if common_name not in name else ""
			if not only:
				for key in thing:
					oname = thing[key]['official']
					official_name = obj['name']['common']
					name += oname if name == "" else ", " + oname if oname not in name else ""
					name += official_name if name == "" else ", " + official_name if official_name not in name else ""
			return name
		linenumber, linecheck = [], []

		# create search list
		lookup = nativenames().split(", ") if nativenames() is not "" else []
		for key in obj['altSpellings']:
			lookup.append(key)
		def findstr(lookup):
			with codecs.open(cur, encoding="utf-8") as c:
			    for num, line in enumerate(c, -2):
			    	for key in lookup:
				        if ((key in line) and (key not in linenumber)):
				            linenumber.append(num)
			c.close()
		findstr(lookup)

		if linecheck == linenumber:
			continue

		country = {}
		country['official_en_name'] = obj['name']['official']
		country['en-GB'] = obj['name']['common']
		country['en-US'] = obj['name']['common']
		country['country_code'] = obj['cca3']
		country['native_names'] = nativenames(True)
		# country['latlng'] = obj['latlng']
		# language support
		for key in obj['translations']:
			if key == 'deu':
				country['de-DE'] = obj['translations'][key]['common']
			elif key == 'fra':
				country['fr-FR'] = obj['translations'][key]['common']
			elif key == 'por':
				country['pt-PT'] = obj['translations'][key]['common']
			elif key == 'rus':
				country['ru-RU'] = obj['translations'][key]['common']
			elif key == 'spa':
				country['es-ES'] = obj['translations'][key]['common']
			elif key == 'zho':
				country['zh-CN'] = obj['translations'][key]['common']
		# country[]
		country['cid'] = list(OrderedDict.fromkeys(linenumber))
		Data2.append(country)

	Data2 = sorted(Data2, key= operator.itemgetter('cid'))


	def cleanData(Data2):
		i = 1
		m = 0
		rep = 1
		ice = 0
		end = False

		while not end:
			for obj in Data2:
				missing=True
				while missing:
					missing = False
					if i in obj['cid']:
						i+=1
						if i > 223:
							end = True
							rep = False
						continue
					elif i-1 in obj['cid']:
						print '\nduplicate entry:'
						print i-1 ,":", Data2[i-m-2]['cid'] 
						print i , ":",obj['cid']

						if len(obj['cid']) > len(Data2[i-m-2]['cid']):
							Data2[i-m-1]['cid'].remove(i-1)
							print 'removed ', i-1,' from ',Data2[i-m-1]['en-GB'], "'s cids. cid now =", Data2[i-m-1]['cid']
						else:
							Data2[i-m-2]['cid'].remove(i-1)
							print 'removed ', i-1,' from ',Data2[i-m-2]['en-GB'], "'s cids.  cid now =", Data2[i-m-2]['cid']
						m-=1
						print "\n"
					else:
						print i,' is missing'
						missing = True
						i+=1
						m+=1
						continue
					break
		Data2 = sorted(Data2, key= operator.itemgetter('cid'))
		print "\ncountries sorted"
		j=0
		for obj in Data2:
			if obj['en-GB'] == 'Iceland':
				ice = j
			j+=1
		while Data2[ice]['cid'][0] !=89:
			cleanData(Data2)
		Data2[ice]['cid'] = Data2[ice]['cid'][:1] 
		Data2 = sorted(Data2, key= operator.itemgetter('cid'))

		return Data2

	Data2 = cleanData(Data2)
	print "\ncleanup 'Iceland' cid"

	idx = 0
	for obj in Data2:
		obj['cid'] = str(obj['cid'][0])
		obj['id'] = idx
		idx+=1

	with codecs.open(res, 'w', encoding="utf-8") as f2 :
		f2.write(json.dumps(Data2, indent = 4, ensure_ascii = True))
	f2.close()
f.close()
# print "\n"
# with open(res, 'r') as f2:
# 	print f2.read()
# f2.close()