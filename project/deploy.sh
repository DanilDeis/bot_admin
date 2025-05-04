#!/bin/bash

IP_ADDRES='192.168.1.103'

USER='danil'

scp -r ./ "$USER@$IP_ADDRES:/home/danil/"