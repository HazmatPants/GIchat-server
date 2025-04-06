import asyncio
import websockets
import time
import json

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
    if username in disallowed_names:
        await websocket.send(f"username \"{username}\" is not allowed.")

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
                            print(online_users)
                            await websocket.send(json.dumps(online_users))
                    else:
                        print(f"Received: {message_data['message'].strip()} from {message_data['username']}")
                elif message_data["type"] == "file":
                    print(f"Received: {message_data['filename']} from {message_data['username']}")
                if user_message.startswith("/"):
                    if user_message.strip() == "/who": # Command Definitions
                        online_users = [client[0] for client in connected_clients]
                        users = ", ".join(online_users)
                        data = {
                            "username": "server",
                            "message": f"There are {len(online_users)} online: " + users if len(online_users) > 1 else "You're all alone... :(",
                            "event": "srv_message"
                            }
                        await websocket.send(json.dumps(data))
                    elif user_message.strip() == "/srv.info":
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

async def main():
    async with websockets.serve(echo, host, port):
        await asyncio.Future()  # Keeps the server running indefinitely

print(f"Server running on {host}:{port}")
asyncio.run(main())

