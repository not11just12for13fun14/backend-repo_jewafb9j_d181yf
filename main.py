import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Basketball Team API running"}

# Schemas for request bodies
class PlayerIn(BaseModel):
    name: str
    number: int
    position: Optional[str] = None

class MatchIn(BaseModel):
    opponent: str
    date: datetime
    home: bool = True
    team_score: Optional[int] = None
    opponent_score: Optional[int] = None
    notes: Optional[str] = None

class StatlineIn(BaseModel):
    match_id: str
    player_id: str
    points: int = 0
    rebounds: int = 0
    assists: int = 0
    steals: int = 0
    blocks: int = 0
    turnovers: int = 0

# Helper to ensure db available

def require_db():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

# Players
@app.post("/api/players")
def create_player(player: PlayerIn):
    require_db()
    player_id = create_document("player", player)
    return {"id": player_id}

@app.get("/api/players")
def list_players():
    require_db()
    players = get_documents("player")
    for p in players:
        p["id"] = str(p.pop("_id"))
    return players

# Matches
@app.post("/api/matches")
def create_match(match: MatchIn):
    require_db()
    match_id = create_document("match", match)
    return {"id": match_id}

@app.get("/api/matches")
def list_matches():
    require_db()
    matches = get_documents("match")
    for m in matches:
        m["id"] = str(m.pop("_id"))
    return matches

# Stats
@app.post("/api/stats")
def add_statline(stat: StatlineIn):
    require_db()
    # Validate ObjectId format
    try:
        _ = ObjectId(stat.match_id)
        _ = ObjectId(stat.player_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid match_id or player_id")
    stat_id = create_document("statline", stat)
    return {"id": stat_id}

@app.get("/api/stats/by-match/{match_id}")
def get_stats_for_match(match_id: str):
    require_db()
    try:
        _ = ObjectId(match_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid match_id")
    stats = get_documents("statline", {"match_id": match_id})
    for s in stats:
        s["id"] = str(s.pop("_id"))
    return stats

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
