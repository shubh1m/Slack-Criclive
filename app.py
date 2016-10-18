from slackclient import SlackClient
from flask import Flask, request
import os
import time

app = Flask(__name__)

#token = "xoxp-91848767090-91832453094-91914233108-e4c6ccf83f763c7f3620afbcb167d362"
#sc = SlackClient(token)
#print(sc.api_call('api.test'))

TOKEN = "1n4NyiVvw9EPmc1YtnzfLi3D"


@app.route('/', methods=['POST'])
def criclive():
    token = request.values.get('token')
    return(token)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
