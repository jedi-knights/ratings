import csv
import os.path

from datetime import datetime
from typing import Optional
from importlib.metadata import requires
from ratings.log import logger

import click

from ratings.models import Country
from ratings.tgs import get_countries, get_organization_by_id, get_events
from ratings.tgs import get_states
from ratings.tgs import get_organizations
from ratings.tgs import get_matches
from ratings.tgs import get_clubs_by_organization_id
from ratings.tgs import get_events_by_organization_id
from ratings.models.match import Match
from ratings.stats import wins
from ratings.stats import losses
from ratings.stats import ties
from ratings.stats import matches_played
from ratings.stats import goals_for
from ratings.stats import goals_against
from ratings.stats import goal_differential
from ratings.stats import points
from ratings.stats import wp, owp, oowp, rpi
from ratings.stats import record
from ratings.stats import goals_per_match

@click.group()
def cli():
    pass

@click.command()
def countries():
    click.echo('Retrieving countries...')
    countries = get_countries()
    for country in countries:
        click.echo(country)

@click.command()
def states():
    click.echo('Retrieving states...')
    states = get_states()
    for state in states:
        click.echo(state)


@click.command()
def organizations():
    click.echo('Retrieving organizations...')
    organizations = get_organizations()
    for organization in organizations:
        click.echo(organization)


@click.command()
@click.option('-o', '--organization-id', required=True, type=int, help='Specify the organization id.')
def events(organization_id: int):
    click.echo(f'Organization id selected: {organization_id}')
    events = get_events_by_organization_id(organization_id)
    for event in events:
        click.echo(event)

@click.command()
@click.option('-o', '--organization-id', required=True, type=int, help='Specify the organization id.')
def clubs(organization_id: int):
    click.echo(f'Organization id selected: {organization_id}')
    clubs = get_clubs_by_organization_id(organization_id)
    for club in clubs:
        click.echo(club)


@click.command()
@click.option('-g', '--gender', required=True, type=click.Choice(['girls', 'boys']), help='Specify the gender for the matches.')
@click.option('-y', '--year', required=True, type=click.Choice(['07', '08', '09', '10']), help='Specify the year for the matches.')
@click.option('-o', '--organization-id', required=True, type=int, help='Specify the organization id.')
@click.option('--output-file', required=False, type=click.Path(), help='Specify the output file name.')
def matches(gender: str, year: str, organization_id: int, output_file: Optional[str]):
    organization = get_organization_by_id(organization_id)

    if not output_file:
        if organization.id == 22:  # BOYS PRE-ECNL
            output_file = f'matches_boys_{year}_pre_ecnl.csv'
        elif organization.id == 12:  # ECNL Boys
            output_file = f'matches_boys_{year}_ecnl.csv'
        elif organization.id == 16: # ECNL Boys Regional League
            output_file = f'matches_boys_{year}_ecrl.csv'
        elif organization.id == 9:  # ECNL Girls
            output_file = f'matches_girls_{year}_ecnl.csv'
        elif organization.id == 13:  # ECNL Girls Regional League
            output_file = f'matches_girls_{year}_ecrl.csv'
        elif organization.id == 21: # GIRLS PRE_ECNL
            output_file = f'matches_girls_{year}_pre_ecnl.csv'


    if os.path.isfile(output_file):
        click.echo(f'Output file {output_file} already exists. Exiting...')
        return

    click.echo(f'Searching matches for {organization.name} {year}...')

    matches = get_matches(gender, year, organization)

    if output_file:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['match_id', 'home_team', 'home_team_id', 'home_team_club_id', 'away_team', 'away_team_id', 'away_team_club_id', 'home_score', 'away_score', 'date'])
            for match in matches:
                date_only = match.date.strftime('%Y-%m-%d')
                writer.writerow([match.id, match.home_team, match.home_team_id, match.home_team_club_id, match.away_team, match.away_team_id, match.away_team_club_id, match.home_score, match.away_score, date_only])
    else:
        for match in matches:
            click.echo(f'{match.id} - {match.home_team} vs {match.away_team} - {match.home_score}-{match.away_score} on {match.date}')


def get_club_name_from_team_name(team_name: str) -> str:
    parts = team_name.split(' ')
    prefix = parts[:-2]
    result = ' '.join(prefix)
    return result


def get_event_name_from_team(team_item: tuple[str, int, int], organization_id: int) -> Optional[str]:
    events = get_events()

    team_name, team_id, club_id = team_item

    # Read the clubs for the specified organization.
    clubs = get_clubs_by_organization_id(organization_id)

    # Find the club in the list of clubs.
    selected_club = None
    for club in clubs:
        current_club_id = club.id

        if current_club_id == club_id:
            selected_club = club
            break

    if selected_club is None:
        logger.warning(f'Club not found for team {team_name}')
        return None

    # Find the event in the list of events.
    selected_event = None

    for event in events:
        if event.id == selected_club.event_id:
            selected_event = event
            break

    if selected_event is None:
        logger.warning(f'Event not found for club {selected_club.name}')
        return None

    return selected_event.name


def read_matches_from_file(file: str) -> list[Match]:
    matches = []
    with open(file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            match = Match()
            match.id = int(row['match_id'].strip())
            match.home_team = row['home_team'].strip()
            match.home_team_id = int(row['home_team_id'].strip())
            match.home_team_club_id = int(row['home_team_club_id'].strip())
            match.away_team = row['away_team'].strip()
            match.away_team_id = int(row['away_team_id'].strip())
            match.away_team_club_id = int(row['away_team_club_id'].strip())
            match.home_score = int(row['home_score'].strip())
            match.away_score = int(row['away_score'].strip())
            match.date = datetime.strptime(row['date'].strip(), '%Y-%m-%d')
            matches.append(match)
    return matches

def calculate_team_stats(matches: list[Match], teams: list[tuple[str, int, int]], organization_id: int) -> dict:
    stats = {}
    for team_item in teams:
        team = team_item[0]
        click.echo(f"Calculating stats for '{team}' ...")
        stats[team] = {
            'wins': wins(matches, team),
            'losses': losses(matches, team),
            'ties': ties(matches, team),
            'matches_played': matches_played(matches, team),
            'goals_for': goals_for(matches, team),
            'goals_against': goals_against(matches, team),
            'goal_differential': goal_differential(matches, team),
            'points': points(matches, team),
            'wp': wp(matches, team, 2),
            'owp': owp(matches, team, 2),
            'oowp': oowp(matches, team, 2),
            'rpi': rpi(matches, team, 2),
            'record': record(matches, team),
            'event_name': get_event_name_from_team(team_item, organization_id),
            'goals_per_match': goals_per_match(matches, team)
        }
    return stats

def sort_teams(teams: list[tuple[str, int, int]], stats: dict) -> list[tuple[str, int, int]]:
    return sorted(teams, key=lambda t: (-stats[t[0]]['rpi'], t[0]))

def collect_teams(matches: list[Match]) -> list[tuple[str, int, int]]:
    teams = set()
    for match in matches:
        teams.add((match.home_team, match.home_team_id, match.home_team_club_id))
        teams.add((match.away_team, match.away_team_id, match.away_team_club_id))
    return sorted(list(teams), key=lambda team: team[0])

def write_stats_to_file(stats_file: str, teams: list[str], stats: dict):
    with open(stats_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['team', 'wins', 'losses', 'ties', 'matches_played', 'goals_for', 'goals_against', 'goal_differential', 'goals_per_match', 'points', 'wp', 'owp', 'oowp', 'rpi', 'event_name', 'record'])
        for team_item in teams:
            team, team_id, club_id = team_item
            team_stats = stats[team]
            writer.writerow([
                team,
                team_stats['wins'],
                team_stats['losses'],
                team_stats['ties'],
                team_stats['matches_played'],
                team_stats['goals_for'],
                team_stats['goals_against'],
                team_stats['goal_differential'],
                team_stats['goals_per_match'],
                team_stats['points'],
                team_stats['wp'],
                team_stats['owp'],
                team_stats['oowp'],
                team_stats['rpi'],
                team_stats['event_name'],
                team_stats['record']
            ])

@click.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True), help='Specify the file to read.')
@click.option('-o', '--organization-id', required=True, type=int, help='Specify the organization id.')
def stats(file: str, organization_id: int):
    click.echo(f'Reading file: {file}')
    matches = read_matches_from_file(file)
    teams = collect_teams(matches)
    stats = calculate_team_stats(matches, teams, organization_id)
    sorted_teams = sort_teams(teams, stats)
    stats_file = file.replace('matches', 'stats')
    write_stats_to_file(stats_file, sorted_teams, stats)


@click.command()
@click.option('-t', '--team', required=True, type=str, help='Specify the team name.')
@click.option('-o', '--organization-id', required=True, type=int, help='Specify the organization id.')
def team2event(team: str, organization_id: int):
    click.echo(get_event_name_from_team(team, organization_id))


cli.add_command(countries)
cli.add_command(states)
cli.add_command(organizations)
cli.add_command(matches)
cli.add_command(clubs)
cli.add_command(events)
cli.add_command(stats)
cli.add_command(team2event)

if __name__ == '__main__':
    cli()
