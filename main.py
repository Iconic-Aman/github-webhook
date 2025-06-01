from flask import Flask, request

app = Flask(__name__)

@app.route('/github', methods=['POST'])
def github_webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event_type == 'push':
        author = payload["pusher"]["name"]
        to_branch = payload["ref"].split("/")[-1]  # refs/heads/main → main
        timestamp = payload["head_commit"]["timestamp"]
        
        print(f'{author} pushed to {to_branch} on {timestamp}')
        return 'Push event received', 200

    return 'Event not handled', 200


if __name__ == '__main__':
    app.run(debug=True)
