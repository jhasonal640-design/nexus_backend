from pydantic import BaseModel

class TournamentCreate(BaseModel):
    name: str

class TournamentJoin(BaseModel):
    tournament_id: str

class TournamentScore(BaseModel):
    tournament_id: str
    score: int

class Notify(BaseModel):
    to: str
    message: str
