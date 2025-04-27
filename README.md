# GI.*chat*

GI.*chat* is a lightweight, easy to set up WebSocket-based chat server written in Python. It's designed for simplicity and efficiency, ideal for chatting with people on your local network, your friends, or anyone!

# Features

- WebSocket-based for real-time communication
- Lightweight and fast with minimal dependencies
- Easy setup, install and run with just a few commands

# Installation

1. Install Python:

```sh
sudo apt install python3
```

2. Clone the repository:

```sh
git clone https://github.com/HazmatPants/GIchat-server.git
cd GIchat-server
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Run the server:

```sh
python3 server.py
```

# Usage

- Connect to the server using the [GI.*chat* client](https://github.com/HazmatPants/GI.chat-client-2.0)
- Default WebSocket URL: ws://localhost:8765
- You can also connect to the official GI.*chat* server at `grigga-industries.ydns.eu`, port `8765`.

# Configuration

Modify `config.json` to change settings like the port and IP.

# Contributing

1. Fork the repository

2. Create a new branch (`git checkout -b <branch-name>`)

3. Commit your changes (`git commit -m "Added feature X"`)

4. Push to the branch (`git push origin <branch-name>`)

5. Open a pull request

# License

[GPL-3.0](https://github.com/HazmatPants/GIchat-server/blob/main/LICENSE)

# Commands

- /who -- Returns all connected clients' usernames.
- /server -- Returns server information, such as the version and uptime.
- /whoami -- Returns your username

## Admin Commands
- !clear -- Clears the message database
