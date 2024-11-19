# Name : Afwan Izzul Fahoil
# No Absence : 2
# Class : XII TKJ 3
import os
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from os.path import join, dirname
from datetime import datetime


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(load_dotenv)

MONGODB_URI = os.environ.get("MONGO_DB")
NAME_DB = os.environ.get("NAME_DB")
client = MongoClient(MONGODB_URI)
db = client[NAME_DB]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=["GET"])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])  
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)


    profile = request.files['profile_give'] 
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)  
    return jsonify({'msg': 'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5500, debug=True) 
