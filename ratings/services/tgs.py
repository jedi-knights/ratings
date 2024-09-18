from ratings.models.country import Country
from ratings.services.countries import get_all_countries
from ratings.database.database import get_session

def get_countries() -> list[Country]:
    """
    Returns a list of countries retrieved from the TGS API.

    This function first fetches country records from a database, then from
    the TGS API if the database returns an empty list of countries.

    :return: A list of countries.
    """
    countries = get_all_countries()

    file_name = 'countries.csv'

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            countries = [Country(int(row[0]), row[1]) for row in reader]
        return countries

    response = requests.get(urljoin(PREFIX, '/api/Association/get-all-countries'))
    response.raise_for_status()

    json_data = response.json()

    selected_countries = []
    for item in json_data.get('data', []):
        current_id = item.get('countryID')
        name = item.get('countryName')

        current_country = Country(id=current_id, name=name)

        selected_countries.append(current_country)

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name'])
        for country in selected_countries:
            writer.writerow([country.id, country.name])

    return selected_countries
