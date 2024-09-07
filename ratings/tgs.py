"""
This module provides a set of functions to interact with the Total Global Sports (TGS) API.

see https://github.com/jedi-knights/ecnl/blob/main/pkg/services/tgs.go
"""
import os
import csv

from urllib.parse import urljoin
from typing import Optional
from enum import StrEnum

import requests

from ratings.models import State, Country, Organization, Club, Team

PREFIX = 'https://public.totalglobalsports.com'

class OrganizationName(StrEnum):
    BOYS_PRE_ECNL = 'BOYS PRE-ECNL'
    ECNL_BOYS = 'ECNL Boys'
    ECNL_BOYS_REGIONAL_LEAGUE = 'ECNL Boys Regional League'
    ECNL_GIRLS = 'ECNL Girls'
    ECNL_GIRLS_REGIONAL_LEAGUE = 'ECNL Girls Regional League'
    GIRLS_PRE_ECNL = 'GIRLS PRE-ECNL'

def get_states() -> list[State]:
    """
    Returns a list of states retrieved from the TGS API.

    :return: A list of states.
    """
    file_name = 'states.csv'

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            states = [State(int(row[0]), row[1]) for row in reader]
        return states

    response = requests.get(urljoin(PREFIX, '/api/Association/get-all-states'))
    response.raise_for_status()

    json_data = response.json()

    selected_states = []
    for item in json_data.get('data', []):
        current_id = item.get('stateID')
        name = item.get('stateName')

        current_state = State(id=current_id, name=name)

        selected_states.append(current_state)


    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name'])
        for state in selected_states:
            writer.writerow([state.id, state.name])

    return selected_states

def get_countries() -> list[Country]:
    """
    Returns a list of countries retrieved from the TGS API.

    :return: A list of countries.
    """
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


def get_organizations(ecnl_only: bool = True) -> list[Organization]:
    """
    Returns a list of organizations retrieved from the TGS API.

    :return: A list of organizations.
    """
    file_name = 'organizations.csv'

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            organizations = [Organization(int(row[0]), int(row[1]), row[2], int(row[3])) for row in reader]
        return organizations

    response = requests.get(urljoin(PREFIX, '/api/Association/get-current-orgs-list'))
    response.raise_for_status()

    json_data = response.json()

    selected_organizations = []
    for item in json_data.get('data', []):
        name = item.get('orgName')

        if ecnl_only and 'ECNL' not in name:
            continue

        current_id = item.get('orgID')
        season_id = item.get('orgSeasonID')
        season_group_id = item.get('orgSeasonGroupID')

        current_organization = Organization(id=current_id, season_id=season_id, name=name, season_group_id=season_group_id)

        selected_organizations.append(current_organization)

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'season_id', 'name', 'season_group_id'])
        for organization in selected_organizations:
            writer.writerow([organization.id, organization.season_id, organization.name, organization.season_group_id])

    return selected_organizations


def get_organization_by_id(target_id: int) -> Optional[Organization]:
    """
    Returns an organization retrieved from the TGS API by ID.

    :param target_id: The ID of the organization.
    :return: An organization.
    """
    for org in get_organizations(ecnl_only=False):
        if org.id == target_id:
            return org

    return None

def get_organization_by_name(target_name: str) -> Optional[Organization]:
    """
    Returns an organization retrieved from the TGS API by name.

    :param target_name: The name of the organization.
    :return: An organization.
    """
    for org in get_organizations(ecnl_only=False):
        if org.name == target_name:
            return org

    return None

def get_clubs_by_organization_id(organization_id: int) -> list[Club]:
    """
    Returns a list of clubs retrieved from the TGS API by organization ID.

    :param organization_id: The ID of the organization.
    :return: A list of clubs.
    """
    file_name = f'clubs_org_{organization_id}.csv'

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            next(reader)

            clubs = []
            for row in reader:
                club = Club()
                club.id = int(row['id'])
                club.name = row['name']
                club.full_name = row['full_name']
                club.city = row['city']
                club.logo = row['logo']
                club.state_code = row['state_code']
                club.org_id = int(row['org_id'])
                club.org_season_id = int(row['org_season_id'])
                club.event_id = int(row['event_id'])

                clubs.append(club)

        return clubs

    response = requests.get(urljoin(PREFIX, f'/api/Event/get-org-club-list-by-orgID-improved/{organization_id}'))
    response.raise_for_status()

    json_data = response.json()

    selected_clubs = []
    for item in json_data.get('data', []):
        current_club = Club()

        current_club.id = item.get('clubID')
        current_club.name = item.get('clubName')
        current_club.full_name = item.get('clubFullName')
        current_club.city = item.get('city')
        current_club.logo = item.get('clubLogo')
        current_club.state_code = item.get('stateCode')
        current_club.org_id = item.get('orgID')
        current_club.org_season_id = item.get('orgSeasonID')
        current_club.event_id = item.get('eventID')

        selected_clubs.append(current_club)

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'full_name', 'city', 'logo', 'state_code', 'org_id', 'org_season_id', 'event_id'])
        for club in selected_clubs:
            writer.writerow([club.id, club.name, club.full_name, club.city, club.logo, club.state_code, club.org_id, club.org_season_id, club.event_id])

    return selected_clubs

def get_clubs_by_organization(organization: Organization) -> list[Club]:
    """
    Returns a list of clubs retrieved from the TGS API by organization.

    :param organization: The organization.
    :return: A list of clubs.
    """
    return get_clubs_by_organization_id(organization.id)

def get_clubs_by_organization_name(organization_name: str) -> list[Club]:
    """
    Returns a list of clubs retrieved from the TGS API by organization name.

    :param organization_name: The name of the organization.
    :return: A list of clubs.
    """
    organization = get_organization_by_name(organization_name)
    return get_clubs_by_organization(organization)


def get_events_by_organization_id(organization_id: int) -> list[int]:
    clubs = get_clubs_by_organization_id(organization_id)

    event_ids = []
    for club in clubs:
        if club.event_id not in event_ids:
            event_ids.append(club.event_id)

    return event_ids


def get_events_by_organization(organization: Organization) -> list[int]:
    """
    Returns a list of events retrieved from the TGS API by organization.

    :param organization: The organization.
    :return: A list of events.
    """
    return get_events_by_organization_id(organization.id)


if __name__ == '__main__':
    states = get_states()
    countries = get_countries()
    organizations = get_organizations(ecnl_only=True)

    organization_clubs = {}
    for organization in organizations:
        clubs = get_clubs_by_organization(organization)
        organization_clubs[organization.name] = clubs

    # for state in states:
    #     print(state)

    # for country in countries:
    #     print(country)

    # for organization in organizations:
    #     print(organization)

    # ecnl_girls_clubs = get_clubs_by_organization_name('ECNL Girls')
    #
    # for club in ecnl_girls_clubs:
    #     print(club.full_name)

    print(get_organization_by_id(9))

