# 🐍 SSH Honeypot 

A realistic SSH honeypot built using Python and Paramiko, designed to simulate an interactive SSH server environment. This honeypot captures login attempts and commands entered by attackers, providing valuable insights into unauthorized access behavior.

---

## 🔒 Features

- Custom fake shell with realistic commands and responses.
- Logs both session activity and user-submitted credentials/commands.
- Simulates a vulnerable SSH environment to attract attackers.
- Lightweight and easy to deploy.
- Uses `RotatingFileHandler` to manage log file sizes.

---

## 📁 File Structure

| File             | Description                                       |
|------------------|---------------------------------------------------|
| `ssh_honeypot.py` | Main honeypot script.                            |
| `code explanation`   | Detailed breakdown of how the honeypot code works and functionality.   |
| `READ.me`       | Documentation file explaining project setup |

---

## 🛠️ Setup Instructions

### 1. 🔑 Generate SSH Host Key

Make sure you generate an SSH RSA key for the honeypot:

```bash
ssh-keygen -t rsa -b 2048 -f ssh_host_key
```
---

### 2. 📦 Install Dependencies

```bash
python3 -m venv honeypot-env
source honeypot-env/bin/activate
pip install paramiko
```
---
### 3. 🚀 Run the Honeypot

```bash
sudo python3 ssh_honeypot.py
```
**Port 2222 is used by default. You can change it by modifying the PORT variable in the script.**
----
## 🧪 Example Interaction
Attacker connects via SSH to port 2222:
```
ssh root@your-ip -p 2222

Fake shell response:
Welcome to Abdullah-BNR
Abdullah-BNR$ whoami
root
Abdullah-BNR$ ls
backup/  secrets.txt  logs/
```
---

### 📄 Logging Overview
| Log File        | Captures                                    |
| --------------- | ------------------------------------------- |
| `audit.log`     | Connection status and shell errors          |
| `cmd_audit.log` | Login credentials, commands run by attacker |

---

### ⚠️ Disclaimer
This project is for educational and research purposes only. Deploying a honeypot on the internet may attract real attackers. Use responsibly and ensure your environment is secure.

## 👨‍💻 Author

Made by [Abdullah Banwair](https://github.com/Rzfn2) — feel free to reach out!

Suggestions, contributions, and pull requests are welcome!
---

# 📄 License
MIT License






