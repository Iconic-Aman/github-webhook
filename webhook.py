import requests, json
webhook_url = "http://127.0.0.1:5000/webhook"

data = {
    "Name": "Aman",
    "Age": 23
}

r = requests.post(url= webhook_url, data= data)

print(r.request.headers)

