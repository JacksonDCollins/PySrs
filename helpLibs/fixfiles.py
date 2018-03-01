import io
import os
import sys
from datetime import datetime, timedelta
import requests
import helpLibs.memrise as memrise



def fix(url, langs):
	linesfromMemrise = memrise.main(url)
	curdate = "{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year)
	returnlist = []
	#try:
	lenr = len(linesfromMemrise)
	for n,i in enumerate(linesfromMemrise):
		levelcount = 1
		i = i.replace("\n", "")
		i = i.split(',')
		i[0] = i[0].replace(",", "commaChar")
		i[1] = i[1].replace(",", "commaChar")
		lang = i[4]
		i[4] = '0'
		i.append("0")
		i.append(curdate)
		i.append("none")
		i.append(curdate)
		i.append("0")
		i.append("")
		i.append(i[2])
		i.append(i[3])
		#i[2] = download(i[0])
		i[3] = "no"
		i.append("no")
		i.append(langs[lang])			
		returnlist.append(i)
	#except Exception as e:
	#	print("dasf", e)
	#	pass
							
						
	tmplist = []
	levelcount = 0
	lastLevel = None
	for l in returnlist:
		if l[12] == lastLevel:
			pass
			#l[3] = "Level{}".format(levelcount)
			#tmplist.append(",".join(l))
		else:
			lastLevel = l[12]
			levelcount += 1
		l[12] = "Level{}".format(levelcount)
		tmplist.append(",".join(l))
	return tmplist

def download(v):
	try:
		r = requests.get("https://cooljugator.com/ru/{}".format(v))
	#print(r.status_code)
	#print(r.headers)
	#print(r.encoding)
		return r.text.split('action.">')[1].split("<")[0]
	except:
		return "none"


#fix()
#print(download("плита"))