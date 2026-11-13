#!/bin/sh
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt
(sleep 5; python3 -m webbrowser http://localhost:8000) &
python3 -m uvicorn app:app --port 8000
