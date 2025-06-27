import logging
import socket
import paramiko
import threading
from logging.handlers import RotatingFileHandler

# === Constants ===
HOST_KEY = paramiko.RSAKey(filename='ssh_host_key')
BIND_ADDR = '0.0.0.0'
PORT = 2222
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt=DATE_FORMAT)

# === Logger: Session Activity ===
Honey_logger = logging.getLogger('Honey_logger')
Honey_logger.setLevel(logging.INFO)
if not Honey_logger.hasHandlers():
    handler = RotatingFileHandler('audit.log', maxBytes=5 * 1024, backupCount=3)
    handler.setFormatter(LOG_FORMAT)
    Honey_logger.addHandler(handler)

# === Logger: Credentials & Commands ===
Honey_logger_creds = logging.getLogger('Honey_logger_creds')
Honey_logger_creds.setLevel(logging.INFO)
if not Honey_logger_creds.hasHandlers():
    creds_handler = RotatingFileHandler('cmd_audit.log', maxBytes=5 * 1024, backupCount=3)
    creds_handler.setFormatter(LOG_FORMAT)
    Honey_logger_creds.addHandler(creds_handler)

# === Emulated Shell ===
def Honey_shell(channel, client_ip):
    ip, port = client_ip
    prompt = "Abdullah-BNR$ "

    fake_responses = {
        "whoami": "root",
        "id": "uid=0(root) gid=0(root) groups=0(root)",
        "ls": "backup/  secrets.txt  logs/",
        "pwd": "/root",
        "uname -a": "Linux Abdullah-BNR 5.15.0 x86_64 GNU/Linux",
        "cat secrets.txt": "root:toor\nadmin:admin123",
        "strings secrets.txt": "CONFIDENTIAL\nadmin_pass\ninternal_key",
        "cd ..": "",
        "cd /": "",
        "clear": "\033c",
    }

    channel.send(b"Welcome to Abdullah-BNR\r\n")
    channel.send((prompt).encode())

    while True:
        try:
            buffer = ""
            while True:
                byte = channel.recv(1).decode("utf-8", errors="ignore")
                if not byte:
                    return

                # Handle Enter key
                if byte in ["\r", "\n"]:
                    cmd = buffer.strip()
                    channel.send("\r\n")
                    break

                # Handle Backspace
                if byte == '\x7f':
                    if buffer:
                        buffer = buffer[:-1]
                        channel.send(b"\b \b")
                    continue

                # Ignore arrow keys (they begin with ESC)
                if byte == '\x1b':
                    channel.recv(2)
                    continue

                buffer += byte
                channel.send(byte.encode())

            if not buffer:
                break

            Honey_logger_creds.info(f"{ip}:{port} >> {cmd}")

            if cmd.lower() in ["exit", "logout", "quit"]:
                channel.send(b"Goodbye\r\n")
                break

            response = fake_responses.get(cmd, f"bash: {cmd}: command not found")
            channel.send((response + "\r\n" + prompt).encode())

        except Exception as e:
            Honey_logger.error(f"{ip}:{port} >> Shell error: {e}")
            break

    channel.close()

# === SSH Server Logic ===
class HoneySSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        ip, port = self.client_ip
        Honey_logger_creds.info(f"{ip}:{port} >> SSH Login: {username}/{password}")
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

# === Client Handler ===
def handle_connection(client, addr):
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        server = HoneySSHServer(addr)
        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel is None:
            Honey_logger.error(f"{addr[0]}:{addr[1]} >> No channel")
            return

        Honey_logger.info(f"{addr[0]}:{addr[1]} >> SSH session started")
        Honey_shell(channel, addr)

    except Exception as e:
        Honey_logger.error(f"{addr[0]}:{addr[1]} >> SSH error: {e}")
    finally:
        try:
            client.close()
        except:
            pass

# === Entry Point ===
def start_ssh_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((BIND_ADDR, PORT))
    sock.listen(100)
    print(f"[+] SSH Honeypot running on {BIND_ADDR}:{PORT}")
    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(client, addr), daemon=True).start()

if __name__ == "__main__":
    start_ssh_server()

