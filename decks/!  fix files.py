import io
import os
import sys
from datetime import datetime, timedelta
import requests

def fix():

	cwd = os.getcwd()

	curdate = "{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year)

	idc = 0
	for doc in os.listdir(cwd):
		if doc.split(".")[1] == "csv" and not doc.split(".")[0] == '!sentences' :
			print(doc)
			if doc.split("-")[0] == "!   fixed":
				with open(doc,'w'): pass
			else:
				with open(doc, "r+", encoding = "utf-8") as f:
					with open("!   fixed- {}".format(doc), 'w', encoding = "utf-8") as t:
						pass
					with open("!   fixed- {}".format(doc), 'r+', encoding = "utf-8") as t:
						returnlist = []
						tmplist = []

						try:
							lenr = len(f.read().split("\n"))
							f.seek(0)
							for n,i in enumerate(f.readlines()):
								levelcount = 1
								i = i.replace("\n", "")
								i = i.split("\t")
								i[0] = i[0].replace(",", "commaChar")
								i[1] = i[1].replace(",", "commaChar")
								if i[2].split(",")[1] == "":
									i.append("Level{}".format(levelcount))
									levelcount += 1
								else:
									i.append(i[2].split(",")[1])
								i[2] = doc.split(".")[0]
								i.append("0")
								i.append("0")
								i.append(curdate)
								i.append("none")
								i.append(curdate)
								i.append("0")
								i.append("")
								i.append(i[2])
								i.append(i[3])
								i[2] = download(i[0])
								print(i[0], i[2], "{}/{}".format(n, lenr))
								i[3] = "yes"
								i.append("no")
								i.append("ru")
								

								tmplist.append(",".join(i))
						except:
							print("dasf")
							pass
							
						for k in range(1,200):
							for line in tmplist:
								line = line.split(",")
								#print(j.split("Level")[1])
								if int(line[12].split("Level")[1]) == k:
									idc += 1
									line[10] = str(idc)
									line[12] = "Level{}".format(k)
									returnlist.append(line)
						
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
						t.write("\n".join(tmplist))

	with open('!sentences.csv', 'w', encoding = "utf-8") as t:
		pass
	with open('!sentences.csv', 'r+', encoding = "utf-8") as t:
		t.write("0SENTENCE,1TRANSLATION,2TAGS,3LEARNED,4ATTEMPTS,5SUCCESFUL ATTEMPS,6DAY LAST ATTEMPT,7LAST ATTEMPT RESULT,8DAY TO REVIEW,9ATTEMPT STREAK,10ID,DECK11,LEVEL12,IGNORE13,LANGUAGE14\n")
	for doc in os.listdir(cwd):
		if doc.split("-")[0] == "!   fixed":
			with open(doc,'r', encoding = 'utf-8') as f:
				print("compile",doc)
				
				with open('!sentences.csv', 'a', encoding = "utf-8") as t:
					t.write(f.read())
					t.write("\n")

	with open('!sentences.csv', 'r+b') as t:
		t.seek(-1,2)
		if t.read() == b'\n':
			size = t.tell()
			t.truncate(size-2)

def download(v):
	try:
		r = requests.get("https://cooljugator.com/ru/{}".format(v))
	#print(r.status_code)
	#print(r.headers)
	#print(r.encoding)
		return r.text.split('action.">')[1].split("<")[0]
	except:
		return "none"


fix()
#print(download("плита"))