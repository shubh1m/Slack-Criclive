from slackclient import SlackClient
from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import json
import os
import time
#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
#sched = BlockingScheduler()
sched = BackgroundScheduler()

URL = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
BASE_URL = "http://www.espncricinfo.com"
API_URL = "https://criclive.herokuapp.com/"


def getHTML(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def getCategories(soup):
    categories = soup.find_all("div", "match-section-head")
    categories = [x.string for x in categories]
    return categories

def getMatches(soup):
    matches = {
            "data": []
            }
    categories = getCategories(soup)
    soup = soup.find(id="live-match-data")
    i=0
    for match_block in soup.find_all("section", "matches-day-block"):
        details = {}
        details = {
                "category": categories[i],
                "matches": []
                }
        i+=1
        for match in match_block.find_all("section", "default-match-block "):
            det = {
                "date": match.find("div", "match-info").find("span", "bold").string,
                "team1": {
                    "name": match.find("div", "innings-info-1").contents[0].strip(),
                    "score": match.find("div", "innings-info-1").contents[1].string
                    },
                "team2": {
                    "name": match.find("div", "innings-info-2").contents[0].strip(),
                    "score": match.find("div", "innings-info-2").contents[1].string
                    },
                "url": BASE_URL + match.find("span", "match-no").find("a").get("href"),
                "status": match.find("div", "match-status").find("span", "bold").string
                }
            if(det["team1"]["score"] or det["team2"]["score"]):
                details["matches"].append(det)
        if(details["matches"]):
            matches["data"].append(details)
    #matches = json.dumps(matches)
    return matches

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
            c_summary.append(summary)
        attachment = {
            "pretext": categories["category"],
            "fields": c_summary
        }
        attachments.append(attachment)

    message = {
            "text": "Live report of all matches",
            "attachments": attachments
        }
    print(type(message))
    return message
    #return json.dumps(message)


@sched.scheduled_job('interval', minutes=1)
@app.route('/', methods=['GET', 'POST'])
def main():
    soup = getHTML(URL)
    allMatches = getMatches(soup)
    results = display(allMatches)
    results = json.dumps(results, indent=4, sort_keys=True)
    return results


'''@app.route('/reply/', methods=['GET','POST'])
def replySlash():
    message = requests.get(API_URL).text
    json.loads(message)
    print(type(message))
    return message
'''

if __name__ == '__main__':
    #global allMatches
    port = int(os.environ.get("PORT", 5000))
    sched.start()
    app.run(host='0.0.0.0', port=port)
