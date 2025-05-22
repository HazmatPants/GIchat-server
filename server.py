from flask import Flask, request, send_from_directory
import threading
import asyncio
import websockets
import time
import json
import os

from db import create_db, save_message, get_all_messages

try:
    SRV_CONFIG = json.loads(open("config.json", "r").read())
    print("loaded config")
except json.JSONDecodeError:
    print("Config is not valid JSON, please check for any mistakes in config.json")
    exit()

def load_blacklist(file_path):
    with open(file_path, "r") as f:
        return [line.strip().lower() for line in f.readlines()]

if SRV_CONFIG["blacklist"]:
    BLACKLIST = load_blacklist("blacklist.txt")
    print(f"loaded {len(BLACKLIST)} words from blacklist")
else:
    print("blacklist is disabled")

SRV_NAME = SRV_CONFIG["name"]
SRV_VERSION = "1.4"
SRV_STARTTIME = time.time()
ADMINKEYS = SRV_CONFIG["admin_keys"]

disallowed_names = ["server", "solari"]

host = SRV_CONFIG["host"]
port = SRV_CONFIG["port"]

connected_clients = set()

def server_info():
    data = {
        "name": SRV_CONFIG["name"],
        "version": SRV_VERSION
    }
    return data

def filter_message(message):
    for word in BLACKLIST:
        message = message.lower().replace(word, "****")
    return message

async def echo(websocket):
    username = await websocket.recv()
    for client in connected_clients:
        if username in client:
            await websocket.send("username is taken")
            return
    if username.lower() in disallowed_names:
        await websocket.send(f"username \"{username}\" is not allowed.")
        return
    elif len(username) > 25:
        await websocket.send(f"username is too long")
        return
    else:
        connected_clients.add((username, websocket)) # Client Connect

    await websocket.send(json.dumps(server_info()))
    print("sent server info to new client")

    for client in connected_clients:
        if client[1] != websocket:
            data = {
                "username": "server",
                "message": username + " has joined",
                "event": "srv_message"
                }
            json_data = json.dumps(data)
            await client[1].send(json_data)

    print(f"Client connected from {websocket.remote_address}")

    try:
        async for message in websocket:
            try:
                message_data = json.loads(message)
                username = message_data.get("username", "Unknown")
                user_message = message_data.get("message", "")
                if message_data["type"] == "msg":
                    if message_data["event"] == "request":
                        if message_data["message"] == "RAW:USERLIST":
                            online_users = [client[0] for client in connected_clients]
                            print(f"Received user list request from {message_data['username']}")
                            await websocket.send(json.dumps(online_users))
                        elif message_data["message"] == "RAW:MSGDB":
                            all_messages = get_all_messages()
                            print(f"Received message database request from {message_data['username']}")
                            await websocket.send(json.dumps(all_messages))
                    else:
                        print(f"<{message_data['username']}>\n{message_data['message'].strip()}")
                        if not message_data["message"].startswith("/") or message_data["message"].startswith("!"):
                            save_message(message_data["username"], message_data["message"])
                elif message_data["type"] == "file":
                    print(f"Received: {message_data['filename']} from {message_data['username']}")
                if user_message.startswith("/"): # general commands
                    if user_message.strip() == "/who":
                        online_users = [client[0] for client in connected_clients]
                        users = ", ".join(online_users)
                        data = {
                            "username": "server",
                            "message": f"There are {len(online_users)} online: " + users if len(online_users) > 1 else "You're all alone... :(",
                            "event": "srv_message"
                            }
                        await websocket.send(json.dumps(data))
                    elif user_message.strip() == "/server":
                        data = {
                            "username": "server",
                            "message": f"Server Name: {SRV_CONFIG['name']}\nServer Version: {SRV_VERSION}\nUptime: {time.time() - SRV_STARTTIME}",
                            "event": "srv_message"
                            }
                        await websocket.send(json.dumps(data))
                    else:
                        data = {
                            "username": "server",
                            "message": "Unrecognized command.",
                            "event": "srv_message"
                            }
                        await websocket.send(json.dumps(data))
                elif user_message.startswith("!"): # admin commands
                    if user_message.strip() == "!clear":
                        if message_data['admin_key'] in ADMINKEYS:
                            os.remove("messages.db")
                            create_db()
                            print(f"message DB was cleared by {message_data['username']}")
                            save_message(message_data['username'], "cleared message DB")
                            data = {
                                "type": "msg",
                                "username": "server",
                                "message": "CLEAR_MESSAGE_DB",
                                "event": "srv_command"
                                }
                            for client in connected_clients:
                                    await client[1].send(json.dumps(data))
                    elif user_message.strip().split(" ")[0] == "!kick":
                        if user_message.strip().split(" ")[1] is not None:
                            print(user_message.strip().split(" ")[1])
                            user_to_kick = user_message.strip().split(" ")[1]
                            data = {
                                "type": "msg",
                                "username": "server",
                                "message": "KICK",
                                "event": "srv_command"
                                }
                            for client in connected_clients:
                                if client[0] == user_to_kick:
                                    await client[1].send(json.dumps(data))
                        else:
                            data = {
                                "type": "msg",
                                "username": "server",
                                "message": "You are not authorized to do that.",
                                "event": "srv_message"
                                }
                            await websocket.send(json.dumps(data))
                else:
                    for client in connected_clients: # Send message to all clients
                        if client[1] != websocket:
                            if message_data["type"] == "msg":
                                if SRV_CONFIG["blacklist"]:
                                    message_data["message"] = filter_message(message_data["message"])
                                await client[1].send(json.dumps(message_data))
                            elif message_data["type"] == "file":
                                for client in connected_clients:
                                    if client[1] != websocket:
                                        await client[1].send(json.dumps(message_data))

            except json.JSONDecodeError:
                print("Received invalid JSON data")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally: # Client Disconnect
        clienttoremove = (username, websocket)
        if clienttoremove in connected_clients:
            connected_clients.remove(clienttoremove)
        print(f"Client {websocket.remote_address} disconnected")
        data = {
            "username": "server",
            "message": username + " left",
            "event": "srv_message"
            }
        for client in connected_clients:
                if client[1] != websocket:
                     await client[1].send(json.dumps(data))

http_host = "0.0.0.0"
http_port = 8000

app = Flask(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def hello():
    return "server is running"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_DIR, file.filename))
    return {"status": "ok", "filename": file.filename}, 200

@app.route('/uploads/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

def run_http_server():
    app.run(host=http_host, port=http_port)

threading.Thread(target=run_http_server, daemon=True).start()

async def main():
    create_db()
    print("Initalized database")
    async with websockets.serve(echo, host, port):
        await asyncio.Future()  # Keeps the server running indefinitely

print(f"server running on {host}:{port}")
asyncio.run(main())
