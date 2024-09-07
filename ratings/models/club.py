class Club:
    id: int
    name: str
    full_name: str
    city: str
    logo: str
    state_code: str
    org_id: int
    org_season_id: int
    event_id: int

    def __str__(self):
        return f"Club(id={self.id}, name='{self.name}', full_name='{self.full_name}', city='{self.city}', state_code='{self.state_code}', org_id={self.org_id}, org_season_id={self.org_season_id}, event_id={self.event_id})"

    def __repr__(self):
        return str(self)
