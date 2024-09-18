from sqlmodel import SQLModel, Field
from typing import Optional


class Country(SQLModel, table=True):
    """
    Represents a country.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)

    def __str__(self):
        return f"Country(id={self.id}, name='{self.name}')"

    def __repr__(self):
        return str(self)
