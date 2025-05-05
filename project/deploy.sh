#!/bin/bash

USER="danil"
IP_ADDRESS="192.168.1.103"
DEPLOY_DIR="/home/danil/project"

scp -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no -r ./* danil@192.168.1.103:$DEPLOY_DIR

ssh -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" << EOF
cd $DEPLOY_DIR
cat > .env << EOL
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
CHANNEL_ID=${CHANNEL_ID}
ADMIN_CHAT_ID=${ADMIN_CHAT_ID}
SECRET_KEY=${SECRET_KEY}
BASE_URL=${BASE_URL}
EOL
docker compose build
docker compose up -d
EOF