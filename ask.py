# Grounded explanations: the AI only gets VERIFIED facts from this investigation.
import json, os, re
from pathlib import Path

DATA = Path(__file__).parent / "data"
M = json.loads((DATA / "scene_manifest.json").read_text())
S = json.loads((DATA / "layers.json").read_text())
R = S["results"]
RATIO = round(R["near_river_flagged_percent"] / R["far_from_river_flagged_percent"])

FACTS = {
    "place": "Pagosa Springs, Colorado, along the San Juan River; a 10 km x 10 km study area",
    "radar": "NASA-ISRO NISAR satellite, L-band radar, HH polarization, NISAR Level-2 GCOV product",
    "dates": {"before": "2026-10-14", "after": "2026-10-26"},
    "event": M["event"],
    "method": S["method"] + ". A pixel is 'flagged' if its signal got 3 dB or more brighter or darker.",
    "results": {
        "flagged_brighter_km2": R["flagged_brighter_km2"], "flagged_darker_km2": R["flagged_darker_km2"],
        "percent_flagged_within_200m_of_river": R["near_river_flagged_percent"],
        "percent_flagged_more_than_1km_from_river": R["far_from_river_flagged_percent"],
        "times_more_change_near_river": RATIO,
        "clearest_change": "a long strip next to the river about 3 km south of downtown that got brighter",
        "change_not_explained_by_flood": "a hillside patch far from the river, likely snow, soil moisture, forest or slope effects"},
    "possible_explanations": ["brighter near river: wet banks, mud, flood debris, or a moved river channel",
                              "darker spots: smoother or drier ground, or standing water",
                              "scattered changes far from the river: normal changes such as snow, wet soil, forests or steep slopes"],
    "evidence": ["news reports (NPR Oct 23, AP Nov 2) say the San Juan River flooded Pagosa Springs and crested around Oct 23, 2026",
                 "flagged changes are concentrated along the river"],
    "limitations": S["limitations"],
    "cannot_answer": ["whether a specific street, house or property flooded", "current or future flood risk",
                      "whether it is safe to go somewhere", "any date, place or number not listed in these facts"],
}
FACTS_TEXT = json.dumps(FACTS, indent=2)

SYSTEM = """You explain a radar change map to people who live in flood-prone areas.
Rules:
- Use ONLY the VERIFIED FACTS below. Never invent numbers, dates, places or sources.
- Radar change is evidence of a changed signal, NOT proof of flooding. Never say flooding is confirmed.
- Never say whether a specific street, home or property flooded or is safe. Say the map cannot show that.
- For safety, evacuation or insurance questions: tell the person to follow local emergency officials and official flood maps, and give no other advice.
- If the facts do not answer the question, say so plainly.
- Plain words, no jargon (explain dB as "how much stronger or weaker the radar echo got" if needed). Under 170 words.
- Use exactly these four short headings: What changed / What could explain it / What supports it / What we are not sure about."""

LOCAL = re.compile(r"\b(my|our|street|st|road|rd|avenue|ave|drive|lane|house|home|property|address|neighbou?rhood|block)\b"
                   r"|\b(safe|danger|evacuat\w*|insurance|should i|will it flood|next flood|risk)\b", re.I)


def offline(question):
    if LOCAL.search(question):
        return {"mode": "offline", "answer": (
            "This map cannot tell whether a specific street or home flooded, or whether a place is safe. "
            "It shows where the radar signal changed in 10-meter squares, and a change is not proof of flooding.\n\n"
            "For your home, safety or insurance, please follow your local emergency officials and official flood maps "
            "(for example FEMA's Flood Map Service Center at msc.fema.gov).")}
    intro = ""
    if re.search(r"radar|how does|how do|how can|work|satellite", question, re.I):
        intro = ("Radar sends its own signal to the ground and measures the echo, so it can see through clouds and at night. "
                 "When the ground gets wetter, muddier or rougher, the echo changes.\n\n")
    return {"mode": "offline", "answer": intro + (
        "What changed\n"
        f"Between Oct 14 and Oct 26, 2026, the radar echo changed a lot (3 dB or more) on about {R['flagged_brighter_km2']} km2 that got brighter "
        f"and {R['flagged_darker_km2']} km2 that got darker, inside a 10 km x 10 km area around Pagosa Springs. Near the river (within 200 m) "
        f"{R['near_river_flagged_percent']}% of the ground changed, compared with {R['far_from_river_flagged_percent']}% far from it: about {RATIO} times more.\n\n"
        "What could explain it\n"
        "Brighter strips along the river could be wet banks, mud, debris or a river channel that moved. "
        "Scattered spots far from the river are probably normal changes like snow, wet soil, forests or steep slopes.\n\n"
        "What supports it\n"
        "News reports say the San Juan River flooded Pagosa Springs and crested around Oct 23, 2026, and the changes line up with the river.\n\n"
        "What we are not sure about\n"
        "The after image was taken about 3 days after the flood peak, the two images were processed with different software versions, "
        "and no official flood map was available to check against. These are flagged changes, not confirmed flooding.")}


def answer_question(question):
    question = (question or "").strip()[:500]
    if not question:
        return {"mode": "offline", "answer": "Please type a question about this map."}
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return offline(question)
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        msg = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"), max_tokens=600,
            system=SYSTEM + "\n\nVERIFIED FACTS:\n" + FACTS_TEXT,
            messages=[{"role": "user", "content": question}])
        text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
        return {"mode": "ai", "answer": text}
    except Exception as e:
        out = offline(question)
        out["note"] = "AI was unavailable (" + type(e).__name__ + "), so this is the built-in answer."
        return out
