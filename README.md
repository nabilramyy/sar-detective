---
title: SAR Detective
sdk: docker
app_port: 7860
---

# SAR Detective website

Flood-change map for Pagosa Springs, CO (NISAR radar, Oct 14 vs Oct 26, 2026).

## Run it
You need Python 3.9 or newer.

- Windows: double-click run_windows.bat
- Mac / Linux: run ./run_mac_linux.sh in a terminal

Or by hand:

    pip install -r requirements.txt
    uvicorn app:app --port 8000

Then open http://localhost:8000 (website) or http://localhost:8000/docs (API docs).

## AI answers (optional)
Without a key, the question box gives built-in answers based on the verified facts.
For AI answers, set your Claude API key before starting (never put it in the code):

- Windows:   set ANTHROPIC_API_KEY=your-key
- Mac/Linux: export ANTHROPIC_API_KEY=your-key

## What is inside
- app.py: the server (API + website)
- ask.py: grounded AI explanations
- static/index.html: the website
- data/: map layers, river line, results (layers.json) and scene details (scene_manifest.json)

## Deploy (get a public link)
- Hugging Face Spaces: create a new Space, choose "Docker", upload all files in this folder. The Dockerfile starts the site on port 7860.
- Vercel: import the GitHub repo; Vercel detects FastAPI and runs app.py (no extra config needed).
- Render: create a "Web Service" from a GitHub repo with these files; render.yaml has the settings.
- Add ANTHROPIC_API_KEY as a secret in the hosting settings if you want AI answers. Never commit the key.

## Checks
Checks run during development all passed: layers line up, dates and sources match the radar files, results are reproducible, missing data gives clear errors, the AI refuses unsupported claims, and no API key is stored.

## Team
- Ramy Slait
- Reem Elsayed
- Mohamed Hesham
- Shadw Abdel Aziz
- Habiba Hashem
- Nabil Ramy

## AI-use disclosure
We used Claude (Anthropic) as a coding assistant to help write and debug parts of the Python notebook, web map, and backend. Our team chose the challenge, study area and flood event, selected the NISAR scenes, made the analysis decisions (quality rules, the 3 dB threshold, the river near/far check), reviewed and tested all code, and wrote the conclusions and limitations. The website's question box can use the Claude API to explain the results in plain language; it answers only from our verified results and does not claim that any specific home flooded. All data comes from NASA-ISRO NISAR (via ASF) and OpenStreetMap; no AI-generated data or images are used.

## License
Code: MIT (see LICENSE). Data: see DATA_SOURCES.md.
