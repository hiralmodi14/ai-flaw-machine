import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,FileResponse
from pydantic import BaseModel
from typing import Dict, Any
from challenges import CHALLENGES
from sandbox import sandbox
from agent import agent
# Initialize FastAPI application
app = FastAPI(
    title="OWASP AI Flaw Machine",
    description="Interactive Agentic AI Security & CTF Lab",
    version="1.0.0"
)
# Ensure folders exist and mount static assets
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
class ChatRequest(BaseModel):
    challenge_id: str
    message: str
class FlagRequest(BaseModel):
    challenge_id: str
    flag: str
solved_challenges = set()
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    """Serves the main single-page cyber dashboard."""
    template_file = os.path.join("templates", "index.html")
    if os.path.exists(template_file):
        return FileResponse(template_file)
    return HTMLResponse("<h1> OWASP AI Flaw Machine Web Server Online!</h1><p>templates/index.html is being prepared.</p>")

@app.get("/api/levels")
async def get_all_levels():
    """Returns all 10 OWASP levels for the sidebar browser."""
    catalog = {}
    for cid, data in CHALLENGES.items():
        catalog[cid] = {
            "id": data["id"],
            "title": data["title"],
            "category": data["category"],
            "difficulty": data["difficulty"],
            "points": data["points"],
            "description": data["description"],
            "hints": data["hints"],
            "solved": cid in solved_challenges
        }
    return catalog

@app.post("/api/chat")
async def handle_chat(req: ChatRequest):
    """Processes attack prompts against Ollama and returns live X-Ray telemetry."""
    if req.challenge_id not in CHALLENGES:
        raise HTTPException(status_code=404, detail="Challenge not found")

    challenge = CHALLENGES[req.challenge_id]
    system_prompt = challenge["system_prompt"]

    start_time = time.time()
    # Call real local AI model!
    reply = agent.generate_reply(system_prompt, req.message)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    # Live X-Ray Telemetry for the inspector panel
    telemetry = {
        "execution_time_ms": duration_ms,
        "system_prompt": system_prompt,
        "token_estimate": len(system_prompt.split()) + len(req.message.split()) + 30
    }

    return {
        "reply": reply,
        "telemetry": telemetry
    }

@app.post("/api/flag")
async def verify_flag(req: FlagRequest):
    """Validates user-submitted flags and updates score."""
    challenge = CHALLENGES.get(req.challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    is_correct = req.flag.strip() == challenge["flag"].strip()
    if is_correct:
        solved_challenges.add(req.challenge_id)
        return {
            "correct": True,
            "message": f" Correct! You earned +{challenge['points']} PTS!",
            "points": challenge["points"],
            "solved_count": len(solved_challenges),
            "total_levels": len(CHALLENGES)
        }
    return {
        "correct": False,
        "message": " Incorrect flag. Check your exfiltrated data and try again!"
    }

@app.get("/api/sandbox")
async def get_sandbox_state():
    """Returns live target sandbox state (files, DB products, and emails)."""
    products = sandbox.execute_raw_query("SELECT id, name, price, stock FROM products LIMIT 5")
    return {
        "files": list(sandbox.files.keys()),
        "emails": sandbox.emails,
        "database_products": products
    }
if __name__ == "__main__":
    import uvicorn
    print(" Starting OWASP AI Flaw Machine at http://127.0.0.1:8000\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
