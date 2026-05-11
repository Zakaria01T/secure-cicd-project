#!/bin/bash
pip install -r requirements.txt
python app.py &
sleep 5
echo "App is running!"