from flask import Flask, request, jsonify
import requests
import time
import threading

app = Flask(__name__)
active_tasks = {}

FB_GRAPH_API_URL = "https://graph.facebook.com/v15.0/t_{thread_id"

def send_message(token, recipient_id, message):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return requests.post(FB_GRAPH_API_URL, json=payload, headers=headers)

@app.route("/start_task", methods=["POST"])
def start_task():
    data = request.json
    threading.Thread(target=message_sender, args=(data,)).start()
    return jsonify({"status": "Task started successfully"}), 200

def message_sender(data):
    convo_id = data["convo_id"]
    tokens = data["tokens"]
    messages = data["messages"]
    timer = data["timer"]
    for msg in messages:
        for token in tokens:
            send_message(token, convo_id, msg)
            time.sleep(timer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
