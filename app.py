# BY Arpit ff
# Modified for ARPIT EXP Website Integration

import os
import sys
import time
import json
import random
import socket
import threading
import signal
import asyncio
import ssl
import urllib3
import pytz
import aiohttp
import requests
import firebase_admin
from firebase_admin import credentials, firestore

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from flask import Flask, jsonify, request
from flask_cors import CORS

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf.timestamp_pb2 import Timestamp
from cfonts import render, say

from protobuf_decoder.protobuf_decoder import Parser
from xDL import *
from Pb2 import (
    DEcwHisPErMsG_pb2,
    MajoRLoGinrEs_pb2,
    PorTs_pb2,
    MajoRLoGinrEq_pb2,
    sQ_pb2,
    Team_msg_pb2
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Global Variables ---
ADMIN_UID = "5513136249"
GUEST_UID = "5940248956"
GUEST_PASSWORD = "BD1BDC8FC10F017FE0727DC67D3907EA06DA252936441CD401BFDF755833F107"
region = 'IND'

online_writer = None
whisper_writer = None
stop_auto = False
auto_start_task = None
start_spam_duration = 18
wait_after_match = 10

# =====================================================================
# 🌐 FLASK APP & FIREBASE CONNECTION
# =====================================================================

web_app = Flask(__name__)
CORS(web_app) 

# 🔥 YAHAN APNI NAYI FIREBASE KEY DAALO (Jo aapne abhi banayi hai) 🔥
firebase_creds = {
  "type": "service_account",
  "project_id": "arpit-exp",
  "private_key_id": "YAHAN_NAYI_PRIVATE_KEY_ID_DAALO",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYAHAN_NAYI_PRIVATE_KEY_DAALO\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@arpit-exp.iam.gserviceaccount.com",
  "client_id": "YAHAN_NAYI_CLIENT_ID_DAALO",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "YAHAN_NAYI_CLIENT_X509_CERT_URL_DAALO"
}

# 🔥 YEH LINE ERROR FIX KAREGI 🔥
if "private_key" in firebase_creds:
    key = firebase_creds["private_key"]
    key = key.replace("\\n", "\n")
    key = key.strip()
    if "-----BEGIN PRIVATE KEY-----" in key and "-----END PRIVATE KEY-----" in key:
        header = "-----BEGIN PRIVATE KEY-----"
        footer = "-----END PRIVATE KEY-----"
        key_body = key.replace(header, "").replace(footer, "").strip()
        key_body = "\n".join([key_body[i:i+64] for i in range(0, len(key_body), 64)])
        key = f"{header}\n{key_body}\n{footer}"
    firebase_creds["private_key"] = key

try:
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase Connected")
except Exception as e:
    print(f"❌ Firebase Error: {e}")

loop = asyncio.new_event_loop()
def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()
threading.Thread(target=start_loop, daemon=True).start()

# =====================================================================
# 🤖 BOT FUNCTIONS (Aapke Original Code Se)
# =====================================================================

async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(bytes.fromhex(packet_hex), AES.block_size)).hex()

async def start_auto_packet(key, iv, region):
    return await GeneRaTePk((await CrEaTe_ProTo({1: 9, 2: {1: 12480598706}})).hex(), '0514' if region.lower() == "ind" else "0515", key, iv)

async def leave_squad_packet(key, iv, region):
    return await GeneRaTePk((await CrEaTe_ProTo({1: 7, 2: {1: 12480598706}})).hex(), '0514' if region.lower() == "ind" else "0515", key, iv)

async def join_teamcode_packet(team_code, key, iv, region):
    fields = {1: 4, 2: {4: bytes.fromhex("01090a0b121920"), 5: str(team_code), 6: 6, 8: 1, 9: {2: 800, 6: 11, 8: "1.111.1", 9: 5, 10: 1}}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0514' if region.lower() == "ind" else "0515", key, iv)

async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT and whisper_writer: whisper_writer.write(PacKeT); await whisper_writer.drain()
    elif TypE == 'OnLine' and online_writer: online_writer.write(PacKeT); await online_writer.drain()

async def dl_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except:
            if attempt < max_retries - 1: await asyncio.sleep(0.5)
    return False

async def SEndMsG(H, message, Uid, chat_id, key, iv):
    if H == 0: return await xSEndMsgsQ(message, chat_id, key, iv)
    elif H == 1: return await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    else: return await xSEndMsg(message, 2, Uid, Uid, key, iv)

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer, whisper_writer, insquad, joining_team
    insquad, joining_team, online_writer, whisper_writer = None, False, None, None
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            online_writer.write(bytes.fromhex(AutHToKen))
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break
            online_writer.close(); await online_writer.wait_closed(); online_writer = None
        except: online_writer = None; await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, reconnect_delay=0.5):
    global whisper_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            whisper_writer.write(bytes.fromhex(AutHToKen))
            await whisper_writer.drain()
            ready_event.set()
            while True:
                data = await reader.read(9999)
                if not data: break
            whisper_writer.close(); await whisper_writer.wait_closed(); whisper_writer = None
        except: whisper_writer = None; await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    print("📁 Loading credentials...")
    open_id, access_token = await GeNeRaTeAccEss(GUEST_UID, GUEST_PASSWORD)
    if not open_id: print("❌ Invalid Account"); return None
    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    resp = await MajorLogin(PyL)
    if not resp: print("❌ Banned / Not Registered"); return None
    auth = await DecRypTMajoRLoGin(resp)
    ld = await GetLoginData(auth.url, PyL, auth.token)
    if not ld: print("❌ Error getting ports"); return None
    login_data = await DecRypTLoGinDaTa(ld)
    online_ip, online_port = login_data.Online_IP_Port.split(":")
    chat_ip, chat_port = login_data.AccountIP_Port.split(":")
    auth_token = await xAuThSTarTuP(int(auth.account_uid), auth.token, int(auth.timestamp), auth.key, auth.iv)
    ready = asyncio.Event()
    asyncio.create_task(TcPChaT(chat_ip, chat_port, auth_token, auth.key, auth.iv, login_data, ready, 'IND'))
    asyncio.create_task(TcPOnLine(online_ip, online_port, auth.key, auth.iv, auth_token))
    await ready.wait()
    print("✅ Bot Online")
    return {'key': auth.key, 'iv': auth.iv}

# =====================================================================
# 🚀 BOT RUNNER FOR WEBSITE
# =====================================================================

async def run_bot_for_web(duration_seconds):
    print(f"🎮 Starting Match Loop for {duration_seconds} seconds...")
    
    login_data = await MaiiiinE()
    if not login_data:
        print("❌ Bot Login Failed!")
        return

    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        try:
            team_code = "123456" 
            
            join_packet = await join_teamcode_packet(team_code, login_data['key'], login_data['iv'], 'IND')
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(2)

            start_packet = await start_auto_packet(login_data['key'], login_data['iv'], 'IND')
            for _ in range(5): 
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_packet)
                await asyncio.sleep(0.5)
            
            print("⏳ Playing match...")
            await asyncio.sleep(15) 
            
            leave_packet = await leave_squad_packet(login_data['key'], login_data['iv'], 'IND')
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"Match Error: {e}")
            await asyncio.sleep(5)
            
    print("🛑 Bot stopped.")

# =====================================================================
# 🌐 API ENDPOINTS
# =====================================================================

@web_app.route("/start-bot", methods=["POST"])
def api_start_bot():
    data = request.json
    uid = data.get("uid")
    duration = data.get("duration", 3600)
    
    if not uid:
        return jsonify({"error": "UID required"}), 400

    print(f"🚀 API Request: Starting bot for {duration} seconds")
    asyncio.run_coroutine_threadsafe(run_bot_for_web(duration), loop)
    return jsonify({"status": "success", "message": "Bot started"}), 200

@web_app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "online"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)
