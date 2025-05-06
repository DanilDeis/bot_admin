#!/bin/bash
set -e

USER="root"
IP_ADDRESS="217.25.90.119"
DEPLOY_DIR="/home/danil/project"

echo "Локальные файлы для копирования:"
ls -la
ssh -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" "mkdir -p $DEPLOY_DIR && touch $DEPLOY_DIR/users.db"

scp -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no -r * .[!.]* "$USER@$IP_ADDRESS":$DEPLOY_DIR

ssh -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" << EOF
  set -e
  cd $DEPLOY_DIR
  echo "Содержимое директории после копирования:"
  ls -la
  docker compose build
  docker compose up -d
  docker compose logs --tail=50

  if ! docker ps --filter "name=watchtower" --format '{{.Names}}' | grep -q watchtower; then
    docker run -d \\
      --name watchtower \\
      -v /var/run/docker.sock:/var/run/docker.sock \\
      containrrr/watchtower \\
      --interval 300
  fi
EOF

