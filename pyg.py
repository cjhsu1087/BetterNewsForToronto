from pygoogle import pygoogle

final_message = 'Hi there! This is the BetterNewsForToronto bot!\n\nI heard you guys don\'t like the Toronto Sun, so I\'m here to provide you some better options! Below are five related links that have nothing to do with the Toronto Sun! (Links are not guaranteed to be news articles...sorry!)'
				
g = pygoogle('Teen in TTC spat with Muslims tells his side')
g.pages = 5
gDict = g.search()
gTitles = gDict.keys()
linkCount = 0;
index = 0;
excludeTorontoSun = 'torontosun'
while (linkCount < 5):
	compURL = gDict[gTitles[index]]
	if excludeTorontoSun not in compURL:
		final_message += '\n\n'+gTitles[index]+'\n'+gDict[gTitles[index]] 
		linkCount+=1
		index+=1
	else:
		index+=1
