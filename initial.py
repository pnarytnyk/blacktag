import os
import slackclient
from slackclien import SlackClient as SC


os.environ['slc']=
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
  channel="@pnarytnyk",
  text="Hello from Python! :tada:",
  username='just a prank',
  icon = ':rolling_on_the_floor_laughing:'
)