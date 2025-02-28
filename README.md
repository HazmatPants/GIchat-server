# GIChat

GIChat is a lightweight, easy to set up WebSocket-based chat server written in Python. It's designed for simplicity and efficiency, ideal for chatting with people on your local network, your friends, or anyone!

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

- Connect to the server using the [GIchat client](https://github.com/HazmatPants/GIchat-client)
- Default WebSocket URL: ws://localhost:8765

# Configuration

Modify `config.json` to change settings like the port, IP, or logging preferences.

# Contributing

1. Fork the repository

2. Create a new branch (`git checkout -b <branch-name>`)

3. Commit your changes (`git commit -m "Added feature X"`)

4. Push to the branch (`git push origin <branch-name>`)

5. Open a pull request

# License

[MIT License](https://mit-license.org/)

# Notes

- Ephemeral Messages: Messages are not saved, neither on the client nor the server.

# Commands

- /who -- Returns all connected clients' usernames.
- /srv.info -- Returns server information, such as the version and uptime.
