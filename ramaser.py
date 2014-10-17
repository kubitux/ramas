#!/usr/bin/python
# -*- coding: utf-8 -*-
"""install beautifulsoup4, python-redis"""
import requests
import bs4 as bs
import json

DICO_CREOLE = "dico.json" 

def updateredis():
	f = open(DICO_CREOLE ,"r")
	dico = json.loads(f.read())
	redis_conn = Redis("localhost")
	for kreol in dico:
		redis_conn.set("kreol:%s:%s" % kreol,dico[kreol])

def parsing(mot_french="manger"):
	payload = {'mot2': mot_french}
	r = requests.post("http://www.creole.org/cgi-bin/dico/dictionnaire_creole.pl", data=payload)
	soup = bs.BeautifulSoup(r.text)
	trad = False
	
	try:
		elem = soup.find_all('font')[6]
	except:
		return {}

	if "Francais" in str(elem):
		trad = elem
	else:
		return {}

	trad2= str(trad).split("<br>")
	trad3=[]

	for elem in trad2:
		if ("Francais" in elem) or ("Cr\xc3\xa9ole" in elem):
			trad3.append(elem.split('White"> ')[1])
	if trad3==[]:
		return{}
	#enleve espace et saut de ligne		
	trad3 = [elem.replace("\r\n","") for elem in trad3]

	dico={}

	for mot in trad3:
		index = trad3.index(mot)
		if index%2==0:
			try:	
				dico[mot.replace(" ","").replace("1-","").replace("2-","").replace("3-","").replace("4-","").replace("5-","")]=trad3[index+1]
			except:
				print "ERROR :" + mot_french
				print "trad2 :"
				print trad2
				print "trad3 :"
				print trad3
				print "index="+str(index)

	return dico	

if __name__ == "__main__":

	dico={}
	french=open('liste_francais.txt','r')
	for mot in french.readlines():
		dico.update(parsing(mot))

	with open(DICO_CREOLE, 'w') as f:
		json.dump(dico, f, indent=4)

	f.close()

