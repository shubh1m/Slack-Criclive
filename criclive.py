import time
from slackclient import SlackClient

token = "xoxp-91848767090-91832453094-91914233108-e4c6ccf83f763c7f3620afbcb167d362"
sc = SlackClient(token)

print(sc.api_call('api.test'))

if sc.rtm_connect():
    print()
