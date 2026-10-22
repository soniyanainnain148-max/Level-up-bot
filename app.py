# BY ARPITFF
# Modified for ARPIT EXP Web Integration

import os
import sys
import time
import json
import pickle
import random
import socket
import threading
import signal
import asyncio
import base64
import binascii
import re
import ssl
import urllib3
import jwt
import pytz
import aiohttp
import requests
import firebase_admin
from firebase_admin import credentials, firestore

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from flask import Flask, jsonify, request

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

ADMIN_UID = "5513136249"
GUEST_UID = "5940248956"
GUEST_PASSWORD = "BD1BDC8FC10F017FE0727DC67D3907EA06DA252936441CD401BFDF755833F107"
region = 'IND'

# --- Global Variables ---
online_writer = None
whisper_writer = None
restart_requested = False
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
legendry_cycle_task = None
legendry_cycle_running = False
reject_spam_running = False
insquad = None
joining_team = False
reject_spam_task = None
lag_running = False
lag_task = None
evo_cycle_running = False
evo_cycle_task = None
auto_start_running = False
auto_start_teamcode = None
stop_auto = False
auto_start_task = None
start_spam_duration = 18
wait_after_match = 10
start_spam_delay = 0.1
spm_inv_task = None
spm_inv_running = False
emote_hijack = True
PACKET_DELAY_ULTRA_FAST = 0.2
SPAM_REQUESTS = 99
BADGE_REQUESTS = 5
exploit_running = False
exploit_instance = None

# --- Emote & Badge Maps ---
evo_emotes = {
    "1": "909000063", "2": "909000068", "3": "909000075", "4": "909040010",
    "5": "909000081", "6": "909039011", "7": "909000085", "8": "909000090",
    "9": "909000098", "10": "909035007", "11": "909042008", "12": "909041005",
    "13": "909033001", "14": "909038010", "15": "909038012", "16": "909045001",
    "17": "909049010", "18": "909051003"
}
EMOTE_MAP = {
    1: 909000063, 2: 909000081, 3: 909000075, 4: 909000085, 5: 909000134,
    6: 909000098, 7: 909035007, 8: 909051012, 9: 909000141, 10: 909034008,
    11: 909051015, 12: 909041002, 13: 909039004, 14: 909042008, 15: 909051014,
    16: 909039012, 17: 909040010, 18: 909035010, 19: 909041005, 20: 909051003,
    21: 909034001
}
LEGENDRY_EMOTE = {
    1: 909051013, 2: 909051014, 3: 909051015, 4: 909051016, 5: 909051017,
    6: 909051020, 7: 909051021, 8: 909051022, 9: 909051023, 10: 909052001,
    11: 909052002, 12: 909052003, 13: 909052004, 14: 909052005, 15: 909052006,
    16: 909052007, 17: 909052008, 18: 909052009, 19: 909052010, 20: 909052011,
    21: 909000037, 22: 909000023
}
BADGE_VALUES = {"s1": 1048576, "s2": 32768, "s3": 2048, "s4": 64, "s5": 262144}

# --- Helper Functions ---
def fixnum(num): return "[C]" + "[C]".join(str(num)) + "[C]"
def format_date_with_month_name(date_str):
    try:
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"):
            try: return datetime.strptime(date_str, fmt).strftime("%d %B %Y")
            except ValueError: continue
        return date_str
    except: return date_str
def dec_to_hex(decimal):
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()

async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(bytes.fromhex(packet_hex), AES.block_size)).hex()

async def base_to_hex(number):
    hex_str = hex(number)[2:]
    if len(hex_str) % 2 != 0: hex_str = '0' + hex_str
    return hex_str.upper()

async def nmnmmmmn(packet_hex, key, iv): return await encrypt_packet(packet_hex, key, iv)

# --- API Functions ---
def send_like(target_uid):
    try:
        url = f"https://freeapisbyadii.vercel.app/api/svc/like?uid={target_uid}&server_name=ind"
        res = requests.get(url, timeout=10)
        if res.status_code != 200: return "[C][B][FF0000]Failed to send like (API error)."
        raw = res.json()
        if not raw.get("success"): return f"[C][B][FF0000]Error: {raw.get('error', 'Unknown')}"
        data = raw.get("data", {})
        likes_given = int(data.get("LikesGivenByAPI", 0))
        styled_uid = fixnum(data.get("UID", target_uid))
        if likes_given <= 0: return f"[C][B][FFA500]Max likes already sent today.\n[C][B][FFFFFF]🆔 UID: {styled_uid}"
        return (f"[C][B]-┌ [FFD700]Like Sent Successfully:\n[FFFFFF]-├─ Name: {data.get('PlayerNickname', 'N/A')}\n"
                f"- ├─ UID: {styled_uid}\n- ├─ Likes Before: {data.get('LikesbeforeCommand', 'N/A')}\n"
                f"- ├─ Likes Given: {likes_given}\n- └─ Likes After: {data.get('LikesafterCommand', 'N/A')}")
    except Exception as e: return f"[C][B][FF0000]Error: {e}"

async def fetch_player_info(session, uid):
    url = f"https://freeapisbyadii.vercel.app/api/svc/player?uid={uid}&region=ind"
    try:
        async with session.get(url) as resp:
            if resp.status != 200: return None
            raw = await resp.json()
            return raw.get("data", {}) if raw.get("success") else None
    except: return None

# --- Core Bot Logic (Your original functions) ---
async def RoomJoin(room_id, password, key, iv):
    try:
        from Pb2.room_join_pb2 import join_room
        root = join_room()
        root.field_1 = 3
        root.field_2.field_1 = int(room_id)
        root.field_2.field_2 = str(password) if password else ""
        root.field_2.field_8.field_1 = "IDC3"
        root.field_2.field_8.field_2 = 149
        root.field_2.field_8.field_3 = "ME"
        root.field_2.field_9 = "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000e\u0016\u0019 \u001d"
        root.field_2.field_10 = 1
        root.field_2.field_13 = 1
        root.field_2.field_14 = 1
        root.field_2.field_16 = "en"
        root.field_2.field_22.field_1 = 21
        encrypted_packet = await encrypt_packet(root.SerializeToString().hex(), key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = hex(packet_length)[2:].upper()
        if len(hex_length) % 2 != 0: hex_length = '0' + hex_length
        if len(hex_length) == 2: header = "0e15000000"
        elif len(hex_length) == 3: header = "0e1500000"
        elif len(hex_length) == 4: header = "0e150000"
        elif len(hex_length) == 5: header = "0e15000"
        else: header = "0e15000000"
        return bytes.fromhex(header + hex_length + encrypted_packet)
    except: return None

async def ArohiAccepted(uid, code, K, V):
    fields = {1: 4, 2: {1: uid, 3: uid, 8: 1, 9: {2: 161, 4: "y[WW", 6: 11, 8: "1.114.18", 9: 3, 10: 1}, 10: str(code)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)

async def get_nickname_from_api(uid):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://freeapisbyadii.vercel.app/api/svc/player?uid={uid}", timeout=10) as res:
                data = await res.json(content_type=None)
                return data.get("data", {}).get("basicInfo", {}).get("nickname", "User")
    except: return "User"

async def start_auto_packet(key, iv, region):
    return await GeneRaTePk((await CrEaTe_ProTo({1: 9, 2: {1: 12480598706}})).hex(), '0514' if region.lower() == "ind" else "0515", key, iv)

async def leave_squad_packet(key, iv, region):
    return await GeneRaTePk((await CrEaTe_ProTo({1: 7, 2: {1: 12480598706}})).hex(), '0514' if region.lower() == "ind" else "0515", key, iv)

async def join_teamcode_packet(team_code, key, iv, region):
    fields = {1: 4, 2: {4: bytes.fromhex("01090a0b121920"), 5: str(team_code), 6: 6, 8: 1, 9: {2: 800, 6: 11, 8: "1.111.1", 9: 5, 10: 1}}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0514' if region.lower() == "ind" else "0515", key, iv)

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(encoded_hex, AES.block_size))

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = "2026-07-09 12:44:05"
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.126.9"
    major_login.system_software = "Android OS 13 / API-33"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "45403"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1280
    major_login.screen_height = 720
    major_login.screen_dpi = "320"
    major_login.processor_details = "ARM64 FP ASIMD AES | 2352 | 8"
    major_login.memory = 128
    major_login.gpu_renderer = "Mali-G610"
    major_login.gpu_version = "OpenGL ES 3.2"
    major_login.unique_device_id = "Google|7a9732a4-2549-4edc-840e-d61263d128f5"
    major_login.client_ip = "162.128.224.168"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    major_login.device_model = "OPPO CPH2217"
    major_login.region = "IND"
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "45403"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "1ac4b80ecf0478a44203bf8fac6120f5"
    major_login.external_storage_total = 20660
    major_login.external_storage_available = 17445
    major_login.internal_storage_total = 2663
    major_login.internal_storage_available = 1500
    major_login.game_disk_storage_available = 17573
    major_login.game_disk_storage_total = 20660
    major_login.external_sdcard_avail_storage = 17573
    major_login.external_sdcard_total_storage = 20660
    major_login.login_by = 3
    major_login.library_path = "/data/app/~~xHaSHUdUBlxvhJaRWh018A==/com.dts.freefireth-4OBn7-sLMoPuswIfmgixhA==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "4c322aeb56444feaa151d1ea91a8f7f2|/data/app"
    major_login.channel_type = 6
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019120816"
    major_login.unknown_int85 = 3
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 25777
    major_login.release_channel = "3rd_party"
    major_login.extra_info = "KqsHTz+zAigQ0BOzKhQHN8ae/IefLXcroDjaj4QY+OF71nTuiQh+myDUqCZFPJQ5gyC9LfEeKoon9d461764VIGguRHcIyKfExGAh4bvxFZRgp2X"
    major_login.extra_json = '{"cur_rate":null,"support_etc2":false}'
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    major_login.unknown_bytes102 = b"E1JMTwcJXjA2"
    return await encrypted_proto(major_login.SerializeToString())

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, ssl=ctx) as response:
            return await response.read() if response.status == 200 else None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {'Authorization': f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, ssl=ctx) as response:
            return await response.read() if response.status == 200 else None

async def DecRypTMajoRLoGin(resp):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes(); proto.ParseFromString(resp); return proto

async def DecRypTLoGinDaTa(data):
    proto = PorTs_pb2.GetLoginData(); proto.ParseFromString(data); return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_packet = await EnC_PacKeT(token.encode().hex(), key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    headers = '0000000' if len(uid_hex) == 9 else ('00000000' if len(uid_hex) == 8 else '000000')
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

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

# --- TCP Connections ---
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer, whisper_writer, insquad, joining_team, uid
    bot_uid = 14572471551
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
                data_hex = data2.hex()
                if data_hex.startswith("0500") and emote_hijack:
                    try:
                        emote_info = await extract_emote_info(data_hex, key, iv)
                        if emote_info and int(emote_info['sender_uid']) != bot_uid:
                            fixed_packet = await Emote_k(int(emote_info['sender_uid']), 909035003, key, iv, region)
                            if fixed_packet: await SEndPacKeT(whisper_writer, online_writer, 'OnLine', fixed_packet)
                    except: pass
                if data_hex.startswith("0500") and insquad is None and not joining_team:
                    try:
                        packet = json.loads(await DeCode_PackEt(data_hex[10:]))
                        squad_owner = packet['5']['data']['1']['data']
                        code = packet['5']['data']['8']['data']
                        invite_uid = packet['5']['data']['2']['data']['1']['data']
                        SendInv = await RedZed_SendInv(bot_uid, invite_uid, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', SendInv)
                        Join = await ArohiAccepted(squad_owner, code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', Join)
                        await asyncio.sleep(2)
                        await auto_hammer_slam_emote_dual(squad_owner, key, iv, region)
                        insquad = True
                        await dl_send_message(0, "Welcome to GENIUS HACKER Bot\nUse /help", squad_owner, squad_owner, key, iv)
                    except: insquad = None; joining_team = False
            online_writer.close(); await online_writer.wait_closed(); online_writer = None
        except: online_writer = None; await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, reconnect_delay=0.5):
    global whisper_writer, uid, chat_id
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            whisper_writer.write(bytes.fromhex(AutHToKen))
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                pK = await AuthClan(LoGinDaTaUncRypTinG.Clan_ID, LoGinDaTaUncRypTinG.Clan_Compiled_Data, key, iv)
                whisper_writer.write(pK); await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                if data.hex().startswith("120000"):
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid, chat_id, inPuTMsG = response.Data.uid, response.Data.Chat_ID, response.Data.msg.lower()
                        
                        if inPuTMsG.strip() == '/help':
                            await dl_send_message(response.Data.chat_type, "[B][C][FFD700]GENIUS HACKER BOT\n[B][C][FFFFFF]/lw <team> - Level Up\n/info <uid> - Player Info", uid, chat_id, key, iv)
                        elif inPuTMsG.strip().startswith('/info '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) == 2:
                                async with aiohttp.ClientSession() as session:
                                    pd = await fetch_player_info(session, parts[1])
                                    if pd: await dl_send_message(response.Data.chat_type, format_player_info(pd), uid, chat_id, key, iv)
                                    else: await dl_send_message(response.Data.chat_type, "❌ Player not found", uid, chat_id, key, iv)
                        elif inPuTMsG.strip().startswith('/lw '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) == 2 and parts[1].isdigit():
                                global auto_start_running, auto_start_teamcode, stop_auto, auto_start_task
                                stop_auto = False; auto_start_running = True; auto_start_teamcode = parts[1]
                                auto_start_task = asyncio.create_task(auto_start_loop(parts[1], uid, chat_id, response.Data.chat_type, key, iv, region))
                                await dl_send_message(response.Data.chat_type, f"✅ Level Up Started for {parts[1]}", uid, chat_id, key, iv)
                        elif inPuTMsG.strip() == '/stop_auto':
                            stop_auto = True
                            await dl_send_message(response.Data.chat_type, "🛑 Level Up Stopped", uid, chat_id, key, iv)
                    except Exception: pass
            whisper_writer.close(); await whisper_writer.wait_closed(); whisper_writer = None
        except: whisper_writer = None; await asyncio.sleep(reconnect_delay)

# --- Main Login Function ---
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
    return {"key": auth.key, "iv": auth.iv, "online_writer": online_writer, "whisper_writer": whisper_writer}


# =====================================================================
# 🌐 NAYA CODE: FLASK API AUR FIREBASE CONNECTION (Website & Render)
# =====================================================================

web_app = Flask(__name__)

# 🔥 YAHAN APNI SERVICE ACCOUNT JSON KEY KA CONTENT DAALO 🔥
firebase_creds = {
  "type": "service_account",
  "project_id": "arpit-exp",
  "private_key_id": "YOUR_PRIVATE_KEY_ID",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxxx@arpit-exp.iam.gserviceaccount.com",
  "client_id": "YOUR_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "YOUR_CLIENT_X509_CERT_URL"
}

try:
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase Connected")
except Exception as e:
    print(f"❌ Firebase Error: {e}")

# Background Loop for Flask
loop = asyncio.new_event_loop()
def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()
threading.Thread(target=start_loop, daemon=True).start()

# API Endpoint
@web_app.route("/start-bot", methods=["POST"])
def api_start_bot():
    data = request.json
    uid = data.get("uid")
    duration = data.get("duration", 3600) # Default 1 ghanta
    
    if not uid:
        return jsonify({"error": "UID required"}), 400

    print(f"🚀 API Request: Starting bot for {duration} seconds")
    
    # Bot ko background mein start karo
    asyncio.run_coroutine_threadsafe(run_bot_for_web(duration, uid), loop)
    
    return jsonify({"status": "success", "message": "Bot started"}), 200

@web_app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "online"})

# Naya Bot Loop (Website ke liye)
async def run_bot_for_web(duration_seconds, customer_uid):
    print(f"🎮 Starting Match Loop for {duration_seconds} seconds for Customer: {customer_uid}")
    
    # Login
    login_data = await MaiiiinE()
    if not login_data:
        print("❌ Bot Login Failed!")
        return

    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        try:
            # Aapka match start logic
            team_code = "123456" # Aap isko change kar sakte ho
            
            join_packet = await join_teamcode_packet(team_code, login_data['key'], login_data['iv'], 'IND')
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(2)

            start_packet = await start_auto_packet(login_data['key'], login_data['iv'], 'IND')
            for _ in range(5): 
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_packet)
                await asyncio.sleep(0.5)
            
            print(f"⏳ Playing match for customer {customer_uid}...")
            await asyncio.sleep(15) 
            
            leave_packet = await leave_squad_packet(login_data['key'], login_data['iv'], 'IND')
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"Match Error: {e}")
            await asyncio.sleep(5)
            
    print(f"🛑 Bot stopped for {customer_uid}")

# =====================================================================
# 🚀 RENDER STARTUP COMMAND
# =====================================================================
if __name__ == '__main__':
    # Render jab is file ko chalayega, toh woh Flask app ko start karega
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)
