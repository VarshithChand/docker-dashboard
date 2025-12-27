Sure — here is the **final clean README.md**, formatted exactly for **copy–paste into GitHub** ⬇️

---

````md
# 🐳 Docker Dashboard – Monitor Running Containers (Flask Web App)

A **simple Container Monitoring Dashboard** built using **Python + Flask**, used to view running Docker containers through a web-based UI.

---

## 🚀 Features
- View all **running Docker containers**
- Shows **Container ID, Image, Created Time, Status**
- Auto-refresh dashboard
- Lightweight – deploy anywhere

---

## 🧰 Tech Stack

| Component  | Description                 |
| ---------- | --------------------------- |
| Python     | Backend                     |
| Flask      | Web Framework               |
| Docker SDK | For interacting with Docker |
| Gunicorn   | Production Web Server       |

---

## 🖥️ Installation – Ubuntu / Linux

### 1️⃣ Update packages
```bash
sudo apt update
````

### 2️⃣ Install required dependencies

```bash
sudo apt install -y python3-pip
sudo apt install -y python3-venv
sudo apt install -y docker.io
```

### 3️⃣ Create project folder & clone repo

```bash
mkdir docker-dashboard
cd docker-dashboard
git clone https://github.com/VarshithChand/docker_dashboard.git .
```

### 4️⃣ Create & activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5️⃣ Install Python requirements

```bash
pip install -r requirements.txt
```

---

## ▶️ Run App (Development)

```bash
python3 app.py
```

The app will start at:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🏭 Run in Production – Gunicorn

```bash
gunicorn -w 1 -b 0.0.0.0:80 app:app
```

Open in browser:

```
http://YOUR_SERVER_IP/
```

---

## 🐳 Docker Status Commands

Make sure Docker is running:

```bash
sudo systemctl start docker
sudo systemctl status docker
```

Check running containers:

```bash
sudo docker ps
```

---

## 🔐 Run App Automatically – Systemd (Optional)

To run dashboard even after reboot:

Create service:

```bash
sudo nano /etc/systemd/system/docker-dashboard.service
```

Paste:

```ini
[Unit]
Description=Docker Dashboard Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/docker-dashboard
Environment="PATH=/home/ubuntu/docker-dashboard/venv/bin"
ExecStart=/home/ubuntu/docker-dashboard/venv/bin/gunicorn -w 1 -b 0.0.0.0:80 app:app

[Install]
WantedBy=multi-user.target
```

Enable & start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable docker-dashboard
sudo systemctl start docker-dashboard
```

---

## 📷 Screenshot

Add a screenshot in your repo and update filename:

```md
![Dashboard Screenshot](screenshot.png)
```

---

## 🤝 Contributing

Pull requests are welcome.
For major changes, open an issue first to discuss.

---

## 📜 License

MIT License

---

⭐ If you like this project, star the repo on GitHub!

```

---

### Want me to:
✔️ Add badges (Flask / Docker / Python)  
✔️ Create auto-install bash script (`install.sh`)  
✔️ Add screenshots preview  

Just say: **"Add badges also"** or **"Give me install.sh script"** 🚀
```
