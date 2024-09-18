# python
from sqlmodel import Session, select
from ratings.models.country import Country


def get_countries(session: Session) -> list[Country]:
    statement = select(Country)
    return session.exec(statement).all()

def get_country_by_id(session: Session, country_id: int) -> Country:
    statement = select(Country).where(Country.id == country_id)
    return session.exec(statement).first()

def get_country_by_name(session: Session, name: str) -> Country:
    statement = select(Country).where(Country.name == name)
    return session.exec(statement).first()

def create_country(session: Session, country: Country):
    session.add(country)
    session.commit()
    session.refresh(country)

    return country
