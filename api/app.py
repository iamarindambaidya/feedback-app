from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to call API

client = MongoClient("mongodb://mongodb:27017/")
db = client["FeedbackDB"]
collection = db["Feedbacks"]

@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = list(collection.find({}, {"_id": 0}))
    return jsonify(feedbacks)

@app.route('/api/feedbacks', methods=['POST'])
def add_feedback():
    data = request.json
    collection.insert_one({
        "name": data["name"],
        "comment": data["comment"]
    })
    return jsonify({"message": "Feedback received"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
