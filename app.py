# BY Arpit ff
# Modified for ARPIT EXP Website Integration (Simulation)

import os
import json
import time
import random
import threading
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app)

def init_firebase():
    if not firebase_admin._apps:
        firebase_key = os.getenv('FIREBASE_KEY')
        if not firebase_key:
            raise Exception("FIREBASE_KEY environment variable not set")
        try:
            config = json.loads(firebase_key)
            if 'private_key' in config:
                config['private_key'] = config['private_key'].replace('\\n', '\n')
            cred = credentials.Certificate(config)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase Init Error: {e}")
            raise e

db = None
def get_db():
    global db
    if db is None:
        init_firebase()
        db = firestore.client()
    return db

loop = asyncio.new_event_loop()
def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()
threading.Thread(target=start_loop, daemon=True).start()

async def run_bot_task(uid, password, duration, userEmail, accountId):
    print(f"[Bot] Login Attempt: {uid}")
    await asyncio.sleep(5)
    print(f"[Bot] Login Successful. Joining Match....")
    
    db = get_db()
    doc_ref = db.collection('bot_accounts').document(accountId)
    
    start_time = time.time()
    while time.time() - start_time < duration:
        await asyncio.sleep(15)
        exp_gain = random.randint(50, 150)
        try:
            doc_ref.update({
                'matchesPlayed': firestore.Increment(1),
                'expGained': firestore.Increment(exp_gain)
            })
            print(f"[Bot] Match Complete. EXP: {exp_gain}")
        except Exception as e:
            print(f"[Bot] Update Error: {e}")
            break

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "online"})

@app.route('/start-bot', methods=['POST'])
def start_bot():
    data = request.get_json()
    uid = data.get('uid')
    password = data.get('password')
    duration = data.get('duration', 3600)
    userEmail = data.get('userEmail')
    accountId = data.get('accountId')

    if not all([uid, password, accountId]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    asyncio.run_coroutine_threadsafe(run_bot_task(uid, password, duration, userEmail, accountId), loop)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
