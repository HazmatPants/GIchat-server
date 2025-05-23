# GIchat

GIchat is a lightweight, easy to set up WebSocket-based chat server written in Python. It's designed for simplicity and efficiency, ideal for chatting with people on your local network, your friends, or anyone!

# Features

- WebSocket-based for real-time communication
- Lightweight and fast with minimal dependencies
- Easy setup, install and run with just a few commands
- Image uploads via HTTP

# Installation

1. Install Python:

```bash
sudo apt install python3
```

2. Clone the repository:

```bash
git clone https://github.com/HazmatPants/GIchat-server.git
cd GIchat-server
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the server:

```bash
python3 server.py
```

# Usage

- Connect to the server using [GIchat client 2.0](https://github.com/HazmatPants/GIchat-client-2.0) or [GIchat Client 1.0](https://github.com/HazmatPants/GI.chat-client-1.0) if PyQt is unavailable for you (1.0 may not work in the future when new features are added)
- You can also connect to the official GIchat server at `grigga-industries.ydns.eu`, port `8765`. (may be down sometimes)

# Configuration

Modify `config.json` to change settings like the port and server name.

# Contributing

1. Fork the repo

2. Clone it to your local machine: `git clone https://github.com/YOUR_USERNAME/YOUR_FORK_NAME.git`

3. Create a new branch: `git checkout -b <BRANCH_NAME>`

4. Make your changes

5. Commit your changes:
```bash
git add .
git commit -m "Feature: added this super cool feature"
```

6. Push to your fork: `git push origin <BRANCH_NAME>`

7. Create a pull request

# License

[GPL-3.0](https://github.com/HazmatPants/GIchat-server/blob/main/LICENSE)

# Commands

- /who -- Returns all connected clients' usernames.
- /server -- Returns server information, such as the name, version, and uptime.
- /whoami -- Returns your username

## Admin Commands
> to setup admin users, add any string of text to the `admin_keys` key in `config.json` then if any client has their admin key in that list, they can execute admin commands.
- !clear -- Clears the message database
- !cleanup -- Deletes images that aren't referenced in the database
- !kick <user> -- Disconnects a user




## To-do's
- Add GUI configuration

### Potential new features
- Profile pictures
- GUI user list
