from sqlmodel import Session, select
from ratings.models.country import Country

def create_country(session: Session, country: Country):
    """
    Create a new country.

    :param session:
    :param country:
    :return:
    """
    session.add(country)
    session.commit()
    session.refresh(country)
    return country

def get_country_by_id(session: Session, country_id: int):
    """
    Get a country by its ID.

    :param session:
    :param country_id:
    :return:
    """
    return session.get(Country, country_id)

def get_country_by_name(session: Session, name: str):
    """
    Get a country by its name.

    :param session:
    :param name:
    :return:
    """
    return session.exec(select(Country).where(Country.name == name)).first()

def get_all_countries(session: Session):
    """
    Get all countries.

    :param session:
    :return:
    """
    statement = select(Country)

    return session.exec(statement).all()

def update_country(session: Session, country_id: int, country_data: dict):
    """
    Update a country by its ID.

    :param session:
    :param country_id:
    :param country_data:
    :return:
    """
    country = session.get(Country, country_id)
    for key, value in country_data.items():
        setattr(country, key, value)

    session.commit()
    session.refresh(country)

    return country

def delete_country(session: Session, country_id: int):
    """
    Delete a country by its ID.

    :param session:
    :param country_id:
    :return:
    """
    country = session.get(Country, country_id)
    if country:
        session.delete(country)
        session.commit()

    return country
