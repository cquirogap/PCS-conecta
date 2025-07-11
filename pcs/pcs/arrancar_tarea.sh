#!/bin/bash
source /home/pcsenv/bin/activate
cd /home/pcs-conecta/pcs
python programador.py >> /var/log/apscheduler_tarea.log 2>&1