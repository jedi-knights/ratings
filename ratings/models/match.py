from datetime import datetime

from typing import Optional

class Match:
    id: int
    home_team: Optional[str]
    away_team: Optional[str]
    home_score: int
    away_score: int
    date: datetime
    meta: dict

    def __init__(self):
        self.id = 0
        self.home_team = None
        self.away_team = None
        self.home_score = 0
        self.away_score = 0
        self.date = datetime.now()
        self.meta = {}

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date} - {self.home_score}-{self.away_score}"

    def __repr__(self):
        return str(self)

    def is_future(self):
        return self.date > datetime.now()

