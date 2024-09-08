import csv

from datetime import datetime
from typing import Optional
from importlib.metadata import requires

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
from ratings.stats import wp
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
def matches(gender: str, year: str, organization_id: int):
    file_name = f'matches_{gender}_{year}_{organization_id}.csv'

    click.echo(f'Gender selected: {gender}')
    click.echo(f'Year selected: {year}')

    organization = get_organization_by_id(organization_id)
    matches = get_matches(gender, year, organization)

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['match_id', 'home_team', 'away_team', 'home_score', 'away_score', 'date'])
        for match in matches:
            date_only = match.date.strftime('%Y-%m-%d')
            writer.writerow([match.id, match.home_team, match.away_team, match.home_score, match.away_score, date_only])


def get_club_name_from_team_name(team_name: str) -> str:
    parts = team_name.split(' ')
    prefix = parts[:-2]
    result = ' '.join(prefix)
    return result


def get_event_name_from_team_name(team_name: str, organization_id: int) -> Optional[str]:
    club_name = get_club_name_from_team_name(team_name)

    clubs_org_file = f'clubs_org_{organization_id}.csv'

    event_id = None
    with open(clubs_org_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == club_name:
                event_id = row['event_id']
                break;

    for event in get_events(ecnl_only=False):
        if event.id == event_id:
            return event.name

    return None


@click.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True), help='Specify the file to read.')
@click.option('-o', '--organization-id', required=True, type=int, help='Specify the organization id.')
def stats(file: str, organization_id: int):
    click.echo(f'Reading file: {file}')



    matches = []
    with open(file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            match = Match()
            match.id = int(row['match_id'].strip())
            match.home_team = row['home_team'].strip()
            match.away_team = row['away_team'].strip()
            match.home_score = int(row['home_score'].strip())
            match.away_score = int(row['away_score'].strip())
            match.date = datetime.strptime(row['date'].strip(), '%Y-%m-%d')

            matches.append(match)


    # Collect all the teams
    teams = set()
    for match in matches:
        teams.add(match.home_team)
        teams.add(match.away_team)

    # Convert teams to a list
    teams = list(teams)

    # Sort the teams by name
    teams.sort()

    # Calculate stats for each team
    stats = {}

    for team in teams:
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
            'wp': wp(matches, team),
            'record': record(matches, team),
            'event_name': get_event_name_from_team_name(team, organization_id),
            'goals_per_match': goals_per_match(matches, team)
        }

    # Sort the teams by points, goal differential, then name
    teams.sort(key=lambda t: (-stats[t]['points'], -goal_differential(matches, t), t))

    # Write the stats to a csv file
    stats_file = file.name.replace('matches', 'stats')
    with open(stats_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['team', 'wins', 'losses', 'ties', 'matches_played', 'goals_for', 'goals_against', 'goal_differential', 'points', 'wp', 'goals_per_match', 'event_name', 'record'])
        for team in teams:
            writer.writerow([team, stats[team]['wins'], stats[team]['losses'], stats[team]['ties'], stats[team]['matches_played'], stats[team]['goals_for'], stats[team]['goals_against'], stats[team]['goal_differential'], stats[team]['points'], stats[team]['wp'], stats[team]['goals_per_match'], stats[team]['event_name'], stats[team]['record']])


@click.command()
@click.option('-t', '--team', required=True, type=str, help='Specify the team name.')
@click.option('-o', '--organization-id', required=True, type=int, help='Specify the organization id.')
def team2event(team: str, organization_id: int):
    click.echo('Retrieving events...')
    events = get_events()
    for event in events:
        click.echo(event)

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
