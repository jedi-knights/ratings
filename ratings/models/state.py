class State:
    """
    Represents a state.
    """
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return f"State(id={self.id}, name='{self.name}')"

    def __repr__(self):
        return str(self)