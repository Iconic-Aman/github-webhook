from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
IST = timezone(timedelta(hours=5, minutes=30))

app = Flask(__name__)

#setup mongodb
client = MongoClient("mongodb://localhost:27017/")
db = client['gihub-webhook']
collection = db['github-events']

def insert_into_mongodb(doc):
    #insert data into mongodb
    collection.insert_one(doc)
    return jsonify({"status": "success"}), 200

@app.route('/github', methods=['POST'])
def github_webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event_type == 'push':
        doc = {
        "request_id": payload['head_commit']['id'],
        "author" : payload["pusher"]["name"],
        "action": "PUSH",
        "from_branch": None,
        "to_branch" : payload["ref"].split("/")[-1], 
        "timestamp" : datetime.now(IST).strftime('%d %B %Y - %I:%M %p UTC')
        }
        print(f'{doc["author"]} submitted a push request from {doc["from_branch"]} to {doc["to_branch"]} on {doc["timestamp"]}')
        insert_into_mongodb(doc)
        return 'PUSH request event received', 200
        
    elif event_type == 'pull_request':
        action = payload.get('action')
        pr = payload.get('pull_request', {})
        if action == 'opened' or action == 'reopened':
            doc = {
            "request_id": str(pr['id']),
            "author" : pr['user']['login'],
            "action": "PULL_REQUEST",
            "from_branch" : pr["head"]["ref"],
            "to_branch" : pr["base"]["ref"],
            "timestamp" : datetime.now(IST).strftime('%d %B %Y - %I:%M %p UTC')
            }
            print(f'{doc["author"]} submitted a pull request from {doc["from_branch"]} to {doc["to_branch"]} on {doc["timestamp"]}')
            insert_into_mongodb(doc)
            return 'Pull request event received', 200
        
        #MERGE request
        elif action == "closed" and pr.get("merged", False):
            doc = {
            "request_id": str(pr['id']),
            "author" : pr['user']['login'],
            "action": "MERGE",
            "from_branch" : pr["head"]["ref"],
            "to_branch" : pr["base"]["ref"],
            "timestamp" : datetime.now(IST).strftime('%d %B %Y - %I:%M %p UTC')
            }
            print(f'{doc["author"]} merged branch {doc["from_branch"]} to {doc["to_branch"]} on {doc["timestamp"]}')
            insert_into_mongodb(doc)
            return 'Pull request merged event received', 200
        else:
            return f"pull request action {doc["action"]} ignored", 200
    else:
        return jsonify({"status": "unhandled event"}), 200
    

        
if __name__ == '__main__':
    app.run(debug=True)
