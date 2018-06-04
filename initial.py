from apscheduler.schedulers.blocking import BlockingScheduler
import os
import slackclient
from slackclient import SlackClient as SC

sched = BlockingScheduler()

os.environ['slc']='xoxp-4120244611-147108286259-374083396053-3a58df311fc7d1d35e396131471a1967'
token = os.environ['slc']
sc=SC(token)

def post_to_chat(chat, mess):
	sc.api_call(
	"chat.postMessage",
	channel="#{}".format(chat),
	text="{}".format(mess),
	username='just a prank',
	icon = ':rolling_on_the_floor_laughing:'
	)

def post_user(user, mess):
	sc.api_call(
	  "chat.postMessage",
	  channel="@{}".format(user),
	  text="{}".format(mess),
	  username='just a prank',
	  icon = ':rolling_on_the_floor_laughing:'
	)

@sched.scheduled_job('interval', minutes=5)
def post_me():
	post_user('pnarytnyk', 'hi bruh, im working')

sched.start()