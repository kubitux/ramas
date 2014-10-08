#!/usr/bin/python
import requests

payload = {'mot1': '', 'mot2': 'valeur'}
r = requests.post("http://www.creole.org/cgi-bin/dico/dictionnaire_creole.pl", data=payload)
print r.text