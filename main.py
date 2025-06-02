from flask import Flask, request
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

#setup mongodb
client = MongoClient("mongodb://localhost:27017/")
db = client['gihub-webhook']
collection = db['github-events']

@app.route('/github', methods=['POST'])
def github_webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event_type == 'push':
        # doc = {
        # "author" : payload["pusher"]["name"],
        # "to_branch" : payload["ref"].split("/")[-1],  
        # "timestamp" : payload["head_commit"]["timestamp"]
        # }
        with open("file1.txt", 'w') as f:
            f.write(str(payload))
        
        
        
 
    # return 'Event not handled', 200 
    elif event_type == 'pull_request':
        action = payload.get('action')
        pr = payload.get('pull_request', {})
        if action == 'opened' or action == 'reopened':
            author = pr['user']['login']
            from_branch = pr["head"]["ref"]
            to_branch = pr["base"]["ref"]
            timestamp = pr["created_at"]
            print(f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}')
            return 'Pull request event received', 200
        #MERGE request
        elif action == "closed" and pr.get("merged", False):
            author = pr['user']['login']
            from_branch = pr["head"]["ref"]
            to_branch = pr["base"]["ref"]
            timestamp = pr["merged_at"]
            print(f'{author} merged branch {from_branch} to {to_branch} on {timestamp}')
            return 'Pull request merged event received', 200
        else:
            return f"pull request action {action} ignored", 200
    else:
        return "Event not handled", 200

        
if __name__ == '__main__':
    app.run(debug=True)
