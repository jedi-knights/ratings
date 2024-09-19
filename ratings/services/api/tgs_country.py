from urllib.parse import urljoin

import requests

from ratings.log import logger
from ratings.constants import TGS_PREFIX
from ratings.models.country import Country

from ratings.services.api.exceptions import TGSAPIError


def get_countries() -> list[Country]:
    """
    Returns a list of countries retrieved from the TGS API.

    This function first fetches country records from a database, then from
    the TGS API if the database returns an empty list of countries.

    :return: A list of countries.
    """
    logger.info("Starting get_countries function")
    resource = '/api/Association/get-all-countries'
    url = urljoin(TGS_PREFIX, url=resource)
    logger.info(f"Requesting URL: '{url}'")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise TGSAPIError(None, f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        raise TGSAPIError(None, f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        raise TGSAPIError(None, f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
        raise TGSAPIError(None, f"An error occurred: {req_err}")

    if response.status_code != 200:
        logger.error(f"Unexpected status code: {response.status_code}")
        raise TGSAPIError(response.status_code)

    try:
        json_data = response.json()
        logger.info(f"Successfully retrieved JSON data")
    except ValueError as err:
        raise TGSAPIError(response.status_code, message=str(err))

    countries = [
        Country(id=item.get('countryID'), name=item.get('countryName'))
        for item in json_data.get('data', [])
    ]

    logger.info(f"Successfully parsed {len(countries)} countries")

    return countries


if __name__ == "__main__":
    try:
        countries = get_countries()

        for country in countries:
            logger.info(country)
    except TGSAPIError as err:
        logger.error(err)

