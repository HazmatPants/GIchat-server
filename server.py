import asyncio
import websockets
import time
import json

def load_blacklist(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]

BLACKLIST = load_blacklist("blacklist.txt")

SRV_CONFIG = json.loads(open("config.json", "r").read())
SRV_VERSION = "1.3"
SRV_STARTTIME = time.time()

host = SRV_CONFIG["host"]
port = SRV_CONFIG["port"]

connected_clients = set()

def filter_message(message):
    for word in BLACKLIST:
        message = message.replace(word, "****")
        return message

async def echo(websocket):
    username = await websocket.recv()
    connected_clients.add((username, websocket))

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

                print(f"Received: {message.strip()} at {time.time():.4f}")
                if user_message.startswith("/"):
                    if user_message.strip() == "/who":
                        online_users = [client[0] for client in connected_clients]
                        users = ", ".join(online_users)
                        print(users)
                        data = {
                            "username": "server",
                            "message": users,
                            "event": "srv_message"
                            }
                        await websocket.send(json.dumps(data))
                    elif user_message.strip() == "/srv.info":
                        data = {
                            "username": "server",
                            "message": f"Server Version: {SRV_VERSION}, Uptime: {time.time() - SRV_STARTTIME}",
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
                    for client in connected_clients:
                        if client[1] != websocket:
                            if SRV_CONFIG["block_bad_words"]:
                                message_data["message"] = filter_message(message_data["message"])
                            await client[1].send(json.dumps(message_data))
                    print(f"Sent data to all: {message_data}")
            except json.JSONDecodeError:
                print("Received invalid JSON data")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clienttoremove = (username, websocket)
        print(clienttoremove)
        print(connected_clients)
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

