class Team:
    def __init__(self, name, rating):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return str(self)

