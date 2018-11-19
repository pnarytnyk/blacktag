import re
import json
import requests
import os
import datetime
import pymongo
import random

#------------------------------------------------------------------------------------------------------------------#
one_day=datetime.timedelta(days=1)

mon_con=os.environ.get('mon_conn',None)
mon_db=os.environ.get('mon_db',None)
cloud=os.environ.get('CLOUDINARY_URL',None)
cname=os.environ.get('C_NAME',None)
shook=os.environ.get('s_hc',None)
s_toc=os.environ.get('s_toc',None)

cl=pymongo.MongoClient(mon_con)
db=cl[mon_db]
us=db.users
l=db.log

users = us.find_one()
log = l.find_one()

cusers = users['users']
clog = log['log']

us_id = users['_id']
log_id = log['_id']


#------------------------------------------------------------------------------------------------------------------#

def is_today_ok(b):
	if b.isocalendar()[2]>5:
		return False
	return True

def is_today_not_cutoff(b):
	if b.isocalendar()[2] == 3 and b.isocalendar()[1]%2 != 0:
		return False
	return True

def send_message(a):
	some_url = f"https://picsum.photos/1000/100/?image={random.randint(1,1050)}"
	if is_today_not_cutoff(datetime.datetime.now().date()):
		payload = {
			  "attachments": [
			    {
			      "link_names": 1,
			      "fallback": "Whos turn will it be today? \nFind out in a message!",
			      "color": "#36a64f",
			      "title": f"Today's standup hero is {a}",
			      "image_url": "some_url"
			    }
			  ]
			}
	else:
		payload = {
			  "attachments": [
			    {
			      "link_names": 1,
			      "fallback": "Noone is gonna be standup hero today, cutof incoming!!!!!",
			      "color": "#36a64f",
			      "title": "Hooray, code cutoff incoming!!!!!!",
			      "image_url": "https://media.giphy.com/media/l3q2sUCenoWY2Cp6U/giphy.gif"
			    }
			  ]
			}
	response = requests.post(
	    shook, data=payload,
	    headers={'Content-Type': 'application/json'}
	)

def update_log(a):
	clog.append(cusers)
	log.update_one({'_id':log_id,},{'$set':{'log':clog}})

def update_user_seq(a=1):
	cusers = cusers[1:]+cusers[:1]
	users.update_one({'_id':us_id,},{'$set':{'users':cusers}})

def refresh_curr_data():
	cl=pymongo.MongoClient(mon_con)
	db=cl[mon_db]
	us=db.users
	l=db.log

	users = us.find_one()['users']
	log = l.find_one()['log']

	cusers = users['users']
	clog = log['log']


if is_today_ok(datetime.datetime.now().date()):
	send_message(cusers[0])
else:
	print('Not today, buddy, not today...')
