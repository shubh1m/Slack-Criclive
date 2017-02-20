from slackclient import SlackClient
from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import json
import os
import time

app = Flask(__name__)

API_URL = "https://criclive-api.herokuapp.com/"

def getHTML(url):
    html_doc = requests.get(url).json()
    return html_doc

#def score(team_score):
#    return lambda s: "Not started" if team_score is None else str(team_score)

def display(matches):
    #matches = json.loads(matches)
    attachments = []
    for categories in matches["data"]:
        c_summary = []
        for match in categories["matches"]:
            summary = {
                "title": match["team1"]["name"] + "-" + str(match["team1"]["score"]) + "  |  " + match["team2"]["name"] + "-" + str(match["team2"]["score"]),
                "value": match["status"],
                #"short": false
            }
            if(match["team1"]["name"] or match["team2"]["name"]):
                c_summary.append(summary)
        if(c_summary):
            attachment = {
                "pretext": categories["category"],
                "fields": c_summary
            }
            attachments.append(attachment)

    message = {
            "text": "Live report of all matches",
            "attachments": attachments
        }
    return message
    #return json.dumps(message)


@app.route('/', methods=['POST'])
def main():
    soup = getHTML(API_URL)
    results = display(soup)
    #results = json.dumps(results, indent=4, sort_keys=True)
    results = json.dumps(results)
    return results


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
