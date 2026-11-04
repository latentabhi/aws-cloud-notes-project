#!/bin/bash
set -e

echo "Updating system..."
sudo apt update -y && sudo apt upgrade -y

echo "Installing python and git..."
sudo apt install -y python3 python3-pip python3-venv git

PROJECT_DIR="$HOME/aws-cloud-notes-project"

if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR" && git pull
else
    echo "Clone your repo to $PROJECT_DIR first."
    exit 1
fi

cd "$PROJECT_DIR"

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env created from template. Update your settings before starting."
fi

echo "Setting up systemd service..."
CURRENT_USER=$(whoami)

sudo tee /etc/systemd/system/cloudnotes.service > /dev/null << EOF
[Unit]
Description=Cloud Notes App
After=network.target

[Service]
User=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python run.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable cloudnotes
sudo systemctl restart cloudnotes

echo "App service is running."
sudo systemctl status cloudnotes --no-pager
