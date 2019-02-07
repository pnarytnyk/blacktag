from jira import JIRA
from github import Github as git 
import re

import json
import requests
import os
import datetime

def is_today_ok(b):
	if b.isocalendar()[2]>5:
		return False
	return True

def is_today_not_cutoff(b):
	if b.isocalendar()[2] == 3 and b.isocalendar()[1]%2 != 0:
		return False
	return True

def print_stuff(a):
	if p_reop:
		a+=':alert: *REOPENS:* :alert:\n'
		for i in p_reop:
			a+=str(i[5]['name'])+ '   {: <52}'.format(i[1])+' {: <16}'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
	a+='*needs testing:*\n'
	if not p_nt:
		a+='\n*NONE*\n'
	for i in p_nt:
		a+=str(i[5]['name'])+ '   {: <52}'.format(i[1])+' {: <16}'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
	
	a+='\n*needs retesting:*\n'
	if not p_nrt:
		a+='\n*NONE*\n'
	for i in p_nrt:
		a+=str(i[5]['name'])+ '   {: <52}'.format(i[1])+' {: <16}'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
	
	a+='\n*testing in progress:*\n'
	if not p_tip:
		a+='\n*NONE*\n'
	for i in p_tip:
		a+=str(i[5]['name'])+ '   {: <52}'.format(i[1])+' {: <16}'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
	
	a+='\n*{} PRs tested, but not merged currently*'.format(len(p_t))
	# a+='\n*tested:*\n'
	# for i in p_t:
	# 	a+=str(i[5]['name'])+ ' {: <55}\t'.format(i[1])+' {: <13}\t'.format(i[2])+'https://chromeriver.atlassian.net/browse/{}'.format(i[4] if i[4] else 'no jira link in PR')+'\n'
	
	return a

devs = ['vpetryk','aivanochko','tkhoma','aromaniv','dhorohotskyi','oziniak','vlevytskyi','tommywoo916','alliecr']
repos = ['mercury', 'tessera-web', 'tessera', 'tessera-validation', 'disney','analytics','customer']
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
reop = r'reopen|blocker'

rep=[ch.get_repo(i) for i in repos]


pulls = [[i.title, i.html_url, i.user.login.lower(), ''.join([jj.name.lower() for jj in list(i.get_labels())]), re.findall(r'(?i)crt-\d{4}',i.title)[0] if re.findall(r'(?i)crt-\d{4}',i.title) else None, j.issue(re.findall(r'(?i)crt-\d{4}',i.title)[0]).raw['fields']['priority'] if re.findall(r'(?i)crt-\d{4}',i.title) else {'name':'HZ','id':'11'}] for k in rep for i in list(k.get_pulls())]
p_nt=sorted(list(filter(lambda x: re.findall(nt, x[3]) and re.findall(r'(?i)crt', x[0]) and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))
p_nrt=sorted(list(filter(lambda x: re.findall(nrt, x[3]) and re.findall(r'(?i)crt', x[0]) and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))
p_t=sorted(list(filter(lambda x: re.findall(t, x[3]) and re.findall(r'(?i)crt', x[0])and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))
p_tip=sorted(list(filter(lambda x: re.findall(tip, x[3]) and re.findall(r'(?i)crt', x[0])and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))
p_reop=sorted(list(filter(lambda x: re.findall(reop, x[3]) and re.findall(r'(?i)crt', x[0])and x[2] in devs, pulls)), key=lambda x: int(x[5]['id']))

sss=''
sss=print_stuff(sss)
# print(sss)
shook=os.environ.get('s_hc',None)
if is_today_ok(datetime.datetime.now().date()):
	response = requests.post(
	    shook, data=json.dumps({'text': sss}),
	    headers={'Content-Type': 'application/json'}
	)
else:
	print('Not today, buddy, not today...')