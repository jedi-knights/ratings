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
from ratings.dict_utils import read_str_value, read_int_value, read_datetime_value

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

def _read_match(record: dict, match: Match) -> Match:
    """
    Reads a match from a dict record.

    :param record: The record to read.
    :param match: The match to populate.
    :return: The populated match.
    """
    match.meta['matchID'] = read_int_value(record, 'matchID')
    match.meta['gameDate'] = read_str_value(record, 'gameDate')
    match.meta['hometeamID'] = read_int_value(record, 'hometeamID')
    match.meta['homeTeamClubID'] = read_int_value(record, 'homeTeamClubID')
    match.meta['awayTeamID'] = read_int_value(record, 'awayTeamID')
    match.meta['awayTeamClubID'] = read_int_value(record, 'awayTeamClubID')
    match.meta['gameTime'] = read_str_value(record, 'gameTime')
    match.meta['flight'] = read_str_value(record, 'flight')
    match.meta['division'] = read_str_value(record, 'division')
    match.meta['homeclublogo'] = read_str_value(record, 'homeclublogo')
    match.meta['awayclublogo'] = read_str_value(record, 'awayclublogo')
    match.meta['homeTeam'] = read_str_value(record, 'homeTeam')
    match.meta['awayTeam'] = read_str_value(record, 'awayTeam')
    match.meta['complex'] = read_str_value(record, 'complex')
    match.meta['venue'] = read_str_value(record, 'venue')
    match.meta['scheduleID'] = read_int_value(record, 'scheduleID')
    match.meta['homeTeamScore'] = read_int_value(record, 'homeTeamScore')
    match.meta['awayTeamScore'] = read_int_value(record, 'awayTeamScore')
    match.meta['eventName'] = read_str_value(record, 'eventName')
    match.meta['eventLogo'] = read_str_value(record, 'eventLogo')
    match.meta['startDate'] = read_datetime_value(record, 'startDate')
    match.meta['endDate'] = read_datetime_value(record, 'endDate')
    match.meta['eventTypeID'] = read_int_value(record, 'eventTypeID')

    match.id = match.meta.get('matchID')
    match.date = match.meta.get('gameDate')
    match.home_team = match.meta.get('homeTeam')
    match.away_team = match.meta.get('awayTeam')
    match.home_score = match.meta.get('homeTeamScore')
    match.away_score = match.meta.get('awayTeamScore')

    return match

def _should_include_match(match: Match, include_future: bool = False) -> bool:
    """
    Determines if a match should be included in the results

    :param match: The match to check.
    :param include_future: Whether to include future matches.
    :return: True if the match should be included, otherwise False.
    """
    if match is None:
        return False

    if match.id <= 0:
        return False

    if not match.is_future():
        return True

    return include_future

def get_match_results_by_club_id_and_event_id(club_id: int, event_id: int, include_future: bool = False) -> list[Match]:
    if club_id == 0 or event_id == 0:
        return []

    response = requests.get(urljoin(PREFIX, f'/api/Club/get-score-reporting-schedule-list/{club_id}/{event_id}'))
    response.raise_for_status()

    json_data = response.json()
    data = json_data.get('data')
    event_past_schedule_list = data.get('eventPastScheduleList')

    matches = []
    match_ids = set()

    for item in event_past_schedule_list:
        match = _read_match(item, Match())

        if not _should_include_match(match, include_future):
            continue

        match_ids.add(match.id)
        matches.append(match)

    return matches


def get_match_results_by_club(club: Club) -> list[Match]:
    return get_match_results_by_club_id_and_event_id(club.id, club.event_id)


def _generate_division(gender: str, year: str) -> str:
    """
    Generates a division based on the gender and year.

    :param: gender
    :param: year
    :return: The division.
    """
    if gender == 'girls':
        return f'G20{year}'

    return f'B20{year}'

def get_matches(gender: str, year: str, organization: Organization) -> list[Match]:
    """
    Returns a list of matches retrieved from the TGS API by gender and year for a specific organization.

    Recall that the organizations are typically
    - ECNL
    - ECNL Regional League
    - Pre-

    """
    clubs = get_clubs_by_organization(organization)

    matches = []
    match_ids = set()

    target_division = _generate_division(gender, year)

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



