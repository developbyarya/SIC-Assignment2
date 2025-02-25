import os
import datetime
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, request

load_dotenv()

ubidots_uri = os.environ["UBIDOTS_URI"]
ubidots_token = os.environ["UBIDOTS_TOKEN"]

client = MongoClient(os.environ["MONGODB_URI"])
db = client.sic

app = Flask(__name__)

@app.get("/hello")
def hello():
    return "Hello"

@app.post("/sensor_data")
def post_sensor_data():
    db.sensors.insert_one({
        "datetime": datetime.datetime.now(tz=datetime.timezone.utc),
        **(request.json)
    })
    result = requests.post(
        ubidots_uri,
        json=request.json,
        headers={
            "X-Auth-Token": ubidots_token
        }
    )
    if result.status_code != 200:
        print(result.json())
        return {
            "status": "cannot send to ubidots"
        }, 400
    return {
        "status": "ok"
    }, 200