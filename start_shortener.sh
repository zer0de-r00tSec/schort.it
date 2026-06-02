#!/bin/bash
cd /home/zer0/schort.it
source venv/bin/activate
nohup uvicorn shortener_app.main:app --log-level error --no-access-log > uvicorn.log 2>&1 &
