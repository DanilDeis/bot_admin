#!/bin/bash

DEPLOY_DIR="/home/danil/project"

scp -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no -r ./* danil@192.168.1.103:$DEPLOY_DIR

# Подключаемся по SSH и запускаем сборку и запуск контейнеров
ssh -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no danil@192.168.1.103 << EOF
  cd $DEPLOY_DIR
  docker compose build
  docker compose up -d
EO
