class Organization:
    """
    Represents an organization.
    """
    id: int
    season_id: int
    name: str
    season_group_id: int

    def __init__(self, id: int, season_id: int, name: str, season_group_id: int):
        self.id = id
        self.season_id = season_id
        self.name = name
        self.season_group_id = season_group_id

    def __str__(self):
        return f"Organization(id={self.id}, season_id={self.season_id}, name='{self.name}', season_group_id={self.season_group_id})"

    def __repr__(self):
        return str(self)
