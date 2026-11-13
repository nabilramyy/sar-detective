# SAR Detective backend - serves ONE precomputed investigation (no on-demand processing)
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ask import answer_question

BASE = Path(__file__).parent
DATA = BASE / "data"
INV = "pagosa-springs-2026-10"
MANIFEST = json.loads((DATA / "scene_manifest.json").read_text())
SUMMARY = json.loads((DATA / "layers.json").read_text())

app = FastAPI(title="SAR Detective API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["*"])
app.mount("/files", StaticFiles(directory=DATA), name="files")


def check(investigation: str):
    if investigation != INV:
        raise HTTPException(404, f"Unknown investigation '{investigation}'. Available: {INV}")


@app.get("/api/health")
def health():
    return {"status": "ok", "investigations": [INV]}


@app.get("/api/investigations")
def investigations():
    return [{"id": INV, "place": "Pagosa Springs, Colorado - San Juan River",
             "before": SUMMARY["dates"]["before"], "after": SUMMARY["dates"]["after"],
             "question": MANIFEST["project_question"]}]


@app.get("/api/scenes")
def scenes(investigation: str = INV):
    check(investigation)
    keep = ["role", "scene_id", "source_link", "acquisition_start_utc", "track", "frame", "orbit_pass_direction",
            "polarization", "radar_band", "processing_version", "maturity"]
    return {"investigation": investigation, "study_area": MANIFEST["study_area"],
            "scenes": [{k: s[k] for k in keep} for s in MANIFEST["scenes"]]}


@app.get("/api/analysis")
def analysis(investigation: str = INV):
    check(investigation)
    return {"investigation": investigation, "method": SUMMARY["method"],
            "settings": MANIFEST["change_detection"], "results": SUMMARY["results"],
            "plain_summary": SUMMARY["plain_summary"], "limitations": SUMMARY["limitations"]}


@app.get("/api/overlays")
def overlays(investigation: str = INV):
    check(investigation)
    files = {"before": "before.png", "after": "after.png", "change": "change_dB.png", "flagged": "flagged_change.png"}
    labels = {l["id"]: l["label"] for l in SUMMARY["layers"]}
    return {"investigation": investigation, "bounds_lat_lon": SUMMARY["bounds_lat_lon"], "crs": "EPSG:4326",
            "layers": [{"id": k, "label": labels[k], "url": f"/files/{v}"} for k, v in files.items()],
            "river_url": "/files/river.geojson", "legend_url": "/files/legend.png"}


class Question(BaseModel):
    question: str
    investigation: str = INV


@app.post("/api/ask")
def ask(q: Question):
    check(q.investigation)
    return answer_question(q.question)


@app.get("/api/reports")
def reports(investigation: str = INV):
    check(investigation)
    return {"investigation": investigation, "title": SUMMARY["title"], "report_url": "/report",
            "summary": SUMMARY["plain_summary"], "dates": SUMMARY["dates"]}


@app.get("/report")
def report():
    return FileResponse(DATA / "report.html")


@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")
