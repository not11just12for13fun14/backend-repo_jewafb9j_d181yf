"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Basketball app schemas

class Player(BaseModel):
    """
    Players collection schema
    Collection: "player"
    """
    name: str = Field(..., description="Player full name")
    number: int = Field(..., ge=0, le=99, description="Jersey number")
    position: Optional[str] = Field(None, description="Position (G, F, C)")

class Match(BaseModel):
    """
    Matches collection schema
    Collection: "match"
    """
    opponent: str = Field(..., description="Opponent team name")
    date: datetime = Field(..., description="Match date and time")
    home: bool = Field(True, description="Home game if true, away if false")
    team_score: Optional[int] = Field(None, ge=0, description="Our team score")
    opponent_score: Optional[int] = Field(None, ge=0, description="Opponent score")
    notes: Optional[str] = Field(None, description="Optional notes")

class Statline(BaseModel):
    """
    Stat lines per player per match
    Collection: "statline"
    """
    match_id: str = Field(..., description="Match ObjectId as string")
    player_id: str = Field(..., description="Player ObjectId as string")
    points: int = Field(0, ge=0)
    rebounds: int = Field(0, ge=0)
    assists: int = Field(0, ge=0)
    steals: int = Field(0, ge=0)
    blocks: int = Field(0, ge=0)
    turnovers: int = Field(0, ge=0)

# Example schemas (kept for reference)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
