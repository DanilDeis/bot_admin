#!/bin/bash

USER="danil"
IP_ADDRESS="192.168.1.103"
DEPLOY_DIR="/home/danil/project"

scp -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no -r ./* danil@192.168.1.103:$DEPLOY_DIR

ssh -i "$HOME/.ssh/key" -o StrictHostKeyChecking=no "$USER@$IP_ADDRESS" << EOF
