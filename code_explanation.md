## 🔍 Full Code Explanation: `ssh_honeypot.py`

This script is a fake SSH server honeypot written in Python using the Paramiko library. It is designed to mimic a real Linux shell experience for attackers and log all activity for threat intelligence purposes.

---

### 📦 Modules & Imports

```python
import logging
import socket
import paramiko
import threading
from logging.handlers import RotatingFileHandler
```

* **paramiko**: Core SSH server functionality.
* **logging**: Captures shell and login activity.
* **threading**: Allows handling multiple SSH clients concurrently.
* **socket**: Listens for SSH connections.
* **RotatingFileHandler**: Prevents log files from growing indefinitely.

---

### ⚙️ Configuration & Constants

```python
HOST_KEY = paramiko.RSAKey(filename='ssh_host_key')
BIND_ADDR = '0.0.0.0'
PORT = 2222
```

* Loads the SSH host key.
* Listens on all interfaces on port 2222.

```python
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = logging.Formatter(...)
```

* Sets up logging format and timestamp style.

---

### 🪵 Logging Setup

Two separate loggers:

```python
Honey_logger = logging.getLogger('Honey_logger')
Honey_logger_creds = logging.getLogger('Honey_logger_creds')
```

* `audit.log`: Tracks session activity.
* `cmd_audit.log`: Logs usernames, passwords, and shell commands.

Both use `RotatingFileHandler` to avoid uncontrolled growth.

---

### 💻 Honey Shell Function

```python
def Honey_shell(channel, client_ip):
```

* Sends a welcome banner and command prompt (`Abdullah-BNR$`).
* Captures keystrokes one at a time.
* Buffers user input until `Enter` is pressed.
* Handles:

  * **Backspace**: deletes last char in buffer.
  * **Arrow keys**: ignored to avoid escape sequence clutter.
  * **Line submission**: logged and processed.

#### Fake Command Handling

```python
fake_responses = {
    "ls": "backup/  secrets.txt  logs/",
    "cat secrets.txt": "root:toor\nadmin:admin123",
    ...
}
```

* Predefined responses for specific commands.
* If the command isn't defined, returns: `bash: <cmd>: command not found`

Each response is followed by the prompt again.

---

### 🔐 SSH Server Logic

```python
class HoneySSHServer(paramiko.ServerInterface):
```

This class accepts and handles authentication + session requests:

* `check_channel_request`: Only allows session channels.
* `check_auth_password`: Always returns successful login and logs the credentials.
* `check_channel_shell_request`: Accepts shell sessions.
* `check_channel_pty_request`: Accepts PTY requests (needed for proper SSH client behavior).

---

### 🔁 Connection Handler

```python
def handle_connection(client, addr):
```

* Sets up SSH transport with the provided `client` socket.
* Loads the `HOST_KEY`.
* Attaches the `HoneySSHServer` class.
* Accepts and hands the connection to `Honey_shell()`.
* Cleans up the socket.

---

### 🚀 Entry Point

```python
def start_ssh_server():
```

* Binds a socket to port 2222.
* Accepts incoming connections.
* For each, launches a new thread with `handle_connection()`.

```python
if __name__ == "__main__":
    start_ssh_server()
```

---

### 🧪 Final Behavior

* Attacker connects via SSH on port 2222.
* Any username/password is accepted.
* A fake Linux shell is shown.
* Commands like `ls`, `pwd`, `cat` are faked.
* All interaction is logged.

---

### 📌 Summary

This honeypot mimics a Linux shell well enough to fool basic attackers and bots. It logs credentials and behavior for analysis, while being safe (no real shell access).

✅ PTY support is enabled.
✅ Echo, backspace, and newline behave normally.
✅ You can enhance it by adding more fake commands or alerts.

---

# 📄 License
MIT License


> ⚠️ **Note:** This honeypot accepts all login attempts and simulates full root access. It should be deployed in a **controlled and isolated environment only**.

---

