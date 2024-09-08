"""
This module provides a set of functions to interact with the Total Global Sports (TGS) API.

see https://github.com/jedi-knights/ecnl/blob/main/pkg/services/tgs.go
"""
import os
import csv

from datetime import datetime
from urllib.parse import urljoin
from typing import Optional
from enum import StrEnum

import requests

from ratings.models import State, Country, Organization, Club, Event, Match

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
        if club.event_id == 0:  # Skip clubs without an event ID
            continue

        if club.event_id not in event_ids:
            event_ids.append(club.event_id)

    event_ids.sort()

    return event_ids


def get_event_ids_by_organization(organization: Organization) -> list[int]:
    """
    Returns a list of events retrieved from the TGS API by organization.

    :param organization: The organization.
    :return: A list of events.
    """
    return get_events_by_organization_id(organization.id)

def get_event_by_id(event_id: int) -> Event:
    response = requests.get(urljoin(PREFIX, f'/api/Event/get-org-event-by-eventID/{event_id}'))
    response.raise_for_status()

    json_data = response.json()
    json_data = json_data.get('data')

    if json_data is None:
        return None

    event = Event()

    event.id = int(json_data.get('eventID'))
    event.name = json_data.get('eventName')
    event.org_id = int(json_data.get('orgID'))
    event.org_name = json_data.get('orgName')
    event.org_season_id = int(json_data.get('orgSeasonID'))
    event.org_season_name = json_data.get('orgSeasonName')

    return event

def get_events_by_organization(organization: Organization) -> list[Event]:
    event_ids = get_event_ids_by_organization(organization)

    events = []
    for event_id in event_ids:
        event = get_event_by_id(event_id)

        if event is None:
            continue

        events.append(event)

    return events


def get_events(ecnl_only: bool = False) -> list[Event]:
    organizations = get_organizations(ecnl_only=ecnl_only)

    events = []
    for organization in organizations:
        organization_events = get_events_by_organization(organization)
        events.extend(organization_events)

    # Sort the events by name
    events.sort(key=lambda x: x.name)

    return events


def get_match_results_by_club_id_and_event_id(club_id: int, event_id: int, include_future: bool = False) -> list[Match]:
    if club_id == 0 or event_id == 0:
        return []

    response = requests.get(urljoin(PREFIX, f'/api/Club/get-score-reporting-schedule-list/{club_id}/{event_id}'))
    response.raise_for_status()

    json_data = response.json()
    json_data = json_data.get('data')
    schedule_list = json_data.get('eventPastScheduleList')

    date_format = '%Y-%m-%dT%H:%M:%S'

    matches = []
    match_ids = set()

    for item in schedule_list:
        match = Match()

        match.meta['matchID'] = item.get('matchID')
        match.meta['gameDate'] = item.get('gameDate', '').strip()
        match.meta['hometeamID'] = item.get('hometeamID')
        match.meta['homeTeamClubID'] = item.get('homeTeamClubID')
        match.meta['awayTeamID'] = item.get('awayTeamID')
        match.meta['awayTeamClubID'] = item.get('awayTeamClubID')
        match.meta['gameTime'] = item.get('gameTime', '').strip()
        match.meta['flight'] = item.get('flight', '').strip()
        match.meta['division'] = item.get('division', '').strip()
        match.meta['homeclublogo'] = item.get('homeclublogo', '').strip()
        match.meta['awayclublogo'] = item.get('awayclublogo', '').strip()
        match.meta['homeTeam'] = item.get('homeTeam', '').strip()
        match.meta['awayTeam'] = item.get('awayTeam', '').strip()
        match.meta['complex'] = item.get('complex')
        match.meta['venue'] = item.get('venue')
        match.meta['scheduleID'] = item.get('scheduleID')
        match.meta['homeTeamScore'] = item.get('homeTeamScore')
        match.meta['awayTeamScore'] = item.get('awayTeamScore')
        match.meta['eventName'] = item.get('eventName', '').strip()
        match.meta['eventLogo'] = item.get('eventLogo', '').strip()
        match.meta['startDate'] = item.get('startDate', '').strip()
        match.meta['endDate'] = item.get('endDate', '').strip()
        match.meta['eventTypeID'] = item.get('eventTypeID')

        match.date = datetime.strptime(match.meta.get('gameDate'), date_format)

        if match.is_future() and not include_future:
            continue

        value = match.meta.get('matchID')
        if value is not None:
            match.id = int(value)
        else:
            match.id = -1

        if match.id <= 0:  # Skip matches without an ID
            continue

        if match.id in match_ids:  # Check if match already exists
            continue

        match.home_team = match.meta.get('homeTeam')
        match.away_team = match.meta.get('awayTeam')

        value = match.meta.get('homeTeamScore')
        if value is not None:
            match.home_score = int(value)
        else:
            match.home_score = 0

        value = match.meta.get('awayTeamScore')
        if value is not None:
            match.away_score = int(value)
        else:
            match.away_score = 0

        match_ids.add(match.id)
        matches.append(match)

    return matches


def get_match_results_by_club(club: Club) -> list[Match]:
    return get_match_results_by_club_id_and_event_id(club.id, club.event_id)


def get_matches(gender: str, year: str, organization: Organization) -> list[Match]:
    clubs = get_clubs_by_organization(organization)

    matches = []
    match_ids = set()

    if gender == 'girls':
        target_division = f'G20{year}'
    else:
        target_division = f'B20{year}'

    for club in clubs:
        club_matches = get_match_results_by_club(club)
        for match in club_matches:
            if match.id in match_ids:
                continue

            if match.meta.get('division') == target_division:
                match_ids.add(match.id)
                matches.append(match)

    return matches


def get_match_results(organization_id: int):
    organization = get_organization_by_id(organization_id)
    clubs = get_clubs_by_organization(organization)

    for club in clubs:
        print(club)



if __name__ == '__main__':
    states = get_states()
    countries = get_countries()
    organizations = get_organizations(ecnl_only=True)

    # organization_clubs = {}
    # for organization in organizations:
    #     clubs = get_clubs_by_organization(organization)
    #     organization_clubs[organization.name] = clubs

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

    # ecnl_girls = get_organization_by_name(OrganizationName.ECNL_GIRLS)
    # events = get_events_by_organization(ecnl_girls)
    #
    # for event in events:
    #     print(event)

    # ecnl_girls_clubs = get_clubs_by_organization(ecnl_girls)
    # results = []
    # for club in ecnl_girls_clubs:
    #     club_results = get_match_results_by_club_id_and_event_id(club_id=club.id, event_id=club.event_id)
    #     if len(club_results) > 0:
    #         results.extend(club_results)
    #
    # for result in results:
    #     print(result)

    events = get_events()
    for event in events:
        print(event)



