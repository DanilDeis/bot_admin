#!/bin/bash

USER="root"
IP_ADDRESS="217.25.90.119"
DEPLOY_DIR="/home/danil/project"

scp -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no -r ./* "$USER@$IP_ADDRESS":$DEPLOY_DIR

ssh -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" << EOF
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 300
cd $DEPLOY_DIR
docker compose build
docker compose up -d
EOF