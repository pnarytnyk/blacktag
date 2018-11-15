from jira import JIRA
from github import Github as git 
import re
import json
import requests
import os
import datetime

def print_stuff(a):
	print('needs testing:')
	a+='*needs testing:*\n'
	for i in p_nt:
		a+=str(i[5]['name'])+ ' {: <55}\t'.format(i[1])+' {: <13}\t'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
		print( i[5]['name'], '{: <60}'.format(i[1])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n')
	a+='\n*needs retesting:*\n'
	for i in p_nrt:
		a+=str(i[5]['name'])+ ' {: <55}\t'.format(i[1])+' {: <13}\t'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
		print( i[5]['name'], '{: <60}'.format(i[1])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n')
	print('\ntesting in progress:')
	a+='\n*testing in progress:*\n'
	for i in p_tip:
		a+=str(i[5]['name'])+ ' {: <55}\t'.format(i[1])+' {: <13}\t'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
		print( i[5]['name'], '{: <60}'.format(i[1]),i[0])
	# print('\ntested:')
	# a+='\n*tested:*\n'
	# for i in p_t:
	# 	a+=str(i[5]['name'])+ ' {: <55}\t'.format(i[1])+' {: <13}\t'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
	# 	print( i[5]['name'], '{: <60}'.format(i[1]),i[0])
	return a

devs = ['vpetryk','aivanochko','tkhoma','aromaniv','dhorohotskyi','oziniak','vlevytskyi','tommywoo916','alliecr']
repos = ['mercury', 'tessera-web', 'tessera', 'tessera-validation', 'disney','analytics']
tkn = os.environ.get('g_tkn',None)
g = git(tkn)
ch=g.get_organization('Chrome-River')

ju=os.environ.get('j_u',None)
jp=os.environ.get('j_p',None)
j = JIRA('https://chromeriver.atlassian.net',
         basic_auth=(ju, jp))

nt = r'needs testing|ready for retesting'
nrt = r'needs retesting'
t = r'tested'
tip = r'testing in progress'

rep=[ch.get_repo(i) for i in repos]


pulls = [[i.title, i.html_url, i.user.login.lower(), ''.join([jj.name.lower() for jj in list(i.get_labels())]), re.findall(r'(?i)crt-\d{4}',i.title)[0] if re.findall(r'(?i)crt-\d{4}',i.title) else None, j.issue(re.findall(r'(?i)crt-\d{4}',i.title)[0]).raw['fields']['priority'] if re.findall(r'(?i)crt-\d{4}',i.title) else {'name':'HZ','id':'11'}] for k in rep for i in list(k.get_pulls())]
p_nt=sorted(list(filter(lambda x: re.findall(nt, x[3]) and re.findall(r'(?i)crt', x[0]) and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))
p_nrt=sorted(list(filter(lambda x: re.findall(nrt, x[3]) and re.findall(r'(?i)crt', x[0]) and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))
p_t=sorted(list(filter(lambda x: re.findall(t, x[3]) and re.findall(r'(?i)crt', x[0])and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))
p_tip=sorted(list(filter(lambda x: re.findall(tip, x[3]) and re.findall(r'(?i)crt', x[0])and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))

sss=''
sss=print_stuff(sss)

shook=os.environ.get('s_hc',None)
response = requests.post(
    shook, data=json.dumps({'text': sss}),
    headers={'Content-Type': 'application/json'}
)
