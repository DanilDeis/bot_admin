#!/bin/bash

USER="root"
IP_ADDRESS="217.25.90.119"
DEPLOY_DIR="/home/danil/project"
ssh -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" "mkdir -p $DEPLOY_DIR"
scp -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no -r ./* "$USER@$IP_ADDRESS":$DEPLOY_DIR

ssh -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" << EOF
 cd $DEPLOY_DIR

  # Используйте docker-compose или docker compose в зависимости от версии
  docker-compose build
  docker-compose up -d

  # Запускаем watchtower, если не запущен
  if ! docker ps --filter "name=watchtower" --format '{{.Names}}' | grep -q watchtower; then
    docker run -d \
      --name watchtower \
      -v /var/run/docker.sock:/var/run/docker.sock \
      containrrr/watchtower \
      --interval 300
  fi
EOF