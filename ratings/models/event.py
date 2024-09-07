class Event:
    id: int
    name: str
    org_id: int
    org_name: str
    org_season_id: int
    org_season_name: str

    def __str__(self) -> str:
        return f"{self.id} - {self.name} ({self.org_name})"

    def __repr__(self) -> str:
        return str(self)
