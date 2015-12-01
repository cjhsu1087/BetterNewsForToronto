whitelist = ['thestar', 'theglobeandmail', 'nationalpost', 'torontosun', 'macleans', 'metronews', 'nowtoronto', 'torontoist', 'blogto', 'cbc', '680news', 'citynews']
compURL = 'www.theglobeandmail.com'
if any(sub in compURL for sub in whitelist):
	print "match!"
else:
	print "no match :("