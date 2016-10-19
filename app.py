from slackclient import SlackClient
from flask import Flask, request
from flask.json import jsonify
from bs4 import BeautifulSoup
import requests
import os
import time

app = Flask(__name__)

TOKEN = "1n4NyiVvw9EPmc1YtnzfLi3D"
URL = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"


def getCategories(soup):
    categories = soup.find_all("div", "match-section-head")
    categories = [x.string for x in categories]
    return categories

def getMatches(soup):
    matches = []
    categories = getCategories(soup)
    soup = soup.find(id="live-match-data")
    i=0
    for match_block in soup.find_all("section", "matches-day-block"):
        details = {}
        details = {
                'category': categories[i],
                'matches': []
                }
        i+=1
        for match in match_block.find_all("section", "default-match-block "):
            det = {
                'dates': match.find("div", "match-info").find("span", "bold").string,
                'team1': {
                    'name': match.find("div", "innings-info-1").contents[0].strip(),
                    'score': match.find("div", "innings-info-1").contents[1].string
                    },
                'team2': {
                    'name': match.find("div", "innings-info-2").contents[0].strip(),
                    'score': match.find("div", "innings-info-2").contents[1].string
                    },
                'status': match.find("div", "match-status").find("span", "bold").string
                }
            details['matches'].append(det)
        matches.append(details)
    return jsonify(matches)


def getHTML(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


@app.route('/', methods=['POST'])
def main():
    token = request.values.get('token')
    if TOKEN == token:
        soup = getHTML(URL)
        matches = getMatches(soup)
        return matches
    else:
        return "Invalid command"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
