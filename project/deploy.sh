#!/bin/bash

USER="root"
IP_ADDRESS="217.25.90.119"
DEPLOY_DIR="/home/danil/project"
START_DIR="/home/danil"
# Создаём директорию и файл users.db на сервере
ssh -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" "mkdir -p $DEPLOY_DIR && touch $DEPLOY_DIR/users.db"

# Копируем все необходимые файлы в директорию проекта на сервере
scp -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no ../docker-compose.yml ../.env ../users.db "$USER@$IP_ADDRESS":$DEPLOY_DIR
scp -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no -r ./* "$USER@$IP_ADDRESS":$DEPLOY_DIR

# Выполняем команды на сервере
ssh -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" << EOF

  cd $START_DIR

  # Строим и запускаем контейнеры
  docker-compose build
  docker-compose up -d

  # Запускаем watchtower, если он не запущен
  if ! docker ps --filter "name=watchtower" --format '{{.Names}}' | grep -q watchtower; then
    docker run -d \
      --name watchtower \
      -v /var/run/docker.sock:/var/run/docker.sock \
      containrrr/watchtower \
      --interval 300
  fi
EOF
