#!/bin/bash

USER="danil"
IP_ADDRESS="192.168.1.103"
DEPLOY_DIR="/home/danil/project"

scp -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no -r ./* danil@192.168.1.103:$DEPLOY_DIR

ssh -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" << EOF
cd $DEPLOY_DIR
cat > .env << EOL
TELEGRAM_BOT_TOKEN=7460006864:AAFSkhVWk0IwgZjK8fuBZx5Jk4F7X_oWkjM
CHANNEL_ID=-1002228367571
ADMIN_CHAT_ID=877631642
SECRET_KEY=11b67d7be7d567a94b2b1bcc612f71e06de31d55d85af8154e552713ee96ae36
BASE_URL=https://payform.ru/u77coTH/
EOL
docker compose build
docker compose up -d
EOF