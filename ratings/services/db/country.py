# python
from sqlmodel import Session, select
from ratings.models.country import Country

def get_country_by_name(session: Session, name: str) -> Country:
    statement = select(Country).where(Country.name == name)
    return session.exec(statement).first()

def create_country(session: Session, country: Country):
    session.add(country)
    session.commit()
    session.refresh(country)

    return country
