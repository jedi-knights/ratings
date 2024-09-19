from ratings.models.country import Country
from ratings.services.countries import get_all_countries
from ratings.services.api.tgs_country import get_countries as fetch_countries_from_tgs
from ratings.database.database import init_db, get_session

def get_countries() -> list[Country]:
    """
    Returns a list of countries, first checking the local database and then
    using the TGS service if no countries are found locally.

    :return: A list of countries.
    """
    session = get_session()
    countries = session.query(Country).all()

    if not countries:
        countries = fetch_countries_from_tgs()
        session.bulk_save_objects(countries)
        session.commit()

    return countries

if __name__ == "__main__":
    init_db()

    countries = get_countries()

    for country in countries:
        print(country)