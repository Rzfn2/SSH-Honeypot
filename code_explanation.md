## 🔍 Full Code Explanation: `ssh_honeypot.py`

This Python script implements a fully functional SSH honeypot using the `paramiko` library. The purpose of the honeypot is to attract malicious actors, log their login attempts and commands, and simulate a fake shell environment that deceives them into thinking they’ve gained access to a legitimate system.

---

### 📦 Modules & Imports

```python
import logging, socket, paramiko, threading
from logging.handlers import RotatingFileHandler
```

- **paramiko**: Handles SSH server functionality.
- **logging**: Records attacker interaction and session details.
- **socket**: Creates TCP socket to listen for SSH connections.
- **threading**: Handles multiple simultaneous SSH connections.
- **RotatingFileHandler**: Keeps log files from growing indefinitely.

---

### ⚙️ Constants & Configuration

```python
HOST_KEY = paramiko.RSAKey(filename='ssh_host_key')
BIND_ADDR = '0.0.0.0'
PORT = 2222
```

- `HOST_KEY`: Load the SSH RSA host key. You must generate this file manually.
- `BIND_ADDR`: Binds the SSH server to all available interfaces.
- `PORT`: The server listens on port 2222 to avoid conflict with real SSH.

---

### 🧾 Log Format Setup

```python
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt=DATE_FORMAT)
```

- Customizes timestamp and format for all log entries.

---

### 🪵 Logging Handlers

```python
Honey_logger = logging.getLogger('Honey_logger')
Honey_logger.setLevel(logging.INFO)
...
Honey_logger_creds = logging.getLogger('Honey_logger_creds')
Honey_logger_creds.setLevel(logging.INFO)
```

- `Honey_logger`: Tracks session-level events (e.g., connection start, errors).
- `Honey_logger_creds`: Logs credentials and commands.
- `RotatingFileHandler`: Creates `audit.log` and `cmd_audit.log` with a size cap of 5 KB and up to 3 backups.

---

### 💻 Simulated Shell Logic

```python
def Honey_shell(channel, client_ip):
```

- Sends welcome banner and prompt (`Abdullah-BNR$`).
- Handles attacker input line-by-line:
  - Commands like `whoami`, `id`, `ls`, `pwd`, and `uname -a` return realistic outputs.
  - Unrecognized input returns: `bash: <cmd>: command not found`
  - Command is logged before the response is returned.
- Exit commands (`exit`, `logout`, `quit`) terminate the session.
- Errors during shell handling are logged.

---

### 🧠 Class: `HoneySSHServer`

```python
class HoneySSHServer(paramiko.ServerInterface):
```

- This class defines the custom SSH server behavior.
- `__init__`: Stores the IP of the connecting client.
- `check_channel_request`: Accepts only `session` channels (standard shell).
- `check_auth_password`: Accepts **any** username/password and logs them.

---

### 🔄 Handling New Connections

```python
def handle_connection(client, addr):
```

- Creates an SSH Transport object.
- Adds the SSH host key (`ssh_host_key`).
- Starts the SSH server with `HoneySSHServer`.
- If authentication succeeds, opens a channel and starts the shell.
- Errors are logged if the connection fails.
- Ensures socket is closed after use.

---

### 🚀 Start the SSH Server

```python
def start_ssh_server():
```

- Creates a socket, binds to the defined IP and port.
- Listens for incoming connections.
- For each connection, spawns a thread that runs `handle_connection()`.

```python
if __name__ == "__main__":
    start_ssh_server()
```

- Ensures the honeypot runs when the script is executed directly.

---

### 📂 File Structure Summary

- `ssh_honeypot.py`: Main script.
- `ssh_host_key`: RSA private key used by Paramiko. Required.
- `audit.log`: Session activity log.
- `cmd_audit.log`: Credential and command log.

---

### ✅ Summary

This script offers a complete simulation of an SSH server to:

- Capture and analyze attacker behavior.
- Log credentials and shell activity.
- Serve as a research or defensive cybersecurity tool.

> ⚠️ **Note:** This honeypot accepts all login attempts and simulates full root access. It should be deployed in a **controlled and isolated environment only**.

---

