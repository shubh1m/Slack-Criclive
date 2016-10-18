import time
from slackclient import SlackClient

token = "xoxp-91848767090-91832453094-91914233108-e4c6ccf83f763c7f3620afbcb167d362"
sc = SlackClient(token)

print(sc.api_call('api.test'))

criclive_token = "1n4NyiVvw9EPmc1YtnzfLi3D"

app = Flask(__name__)

@app.route('/', methods=['POST'])
def criclive():
    text = request.values.get('token')
    print(text)


if __name__ == '__main__':
    app.run()
