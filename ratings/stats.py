"""
This module contains functions that calculate various statistics for a team given a list of matches.
"""

from ratings.models import Match

def wins(matches: list[Match], team: str) -> int:
    """
    Returns the number of wins for a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate wins for.

    Returns:
        int: The number of wins for the given team.
    """
    count = 0
    for match in matches:
        if match.home_team == team and match.home_score > match.away_score:
            count += 1
        elif match.away_team == team and match.away_score > match.home_score:
            count += 1
    return count

def losses(matches: list[Match], team: str) -> int:
    """
    Returns the number of losses for a given team in a list of matches.

    Args:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate losses for.

    Returns:
        int: The number of losses for the given team.
    """
    count = 0
    for match in matches:
        if match.home_team == team and match.home_score < match.away_score:
            count += 1
        elif match.away_team == team and match.away_score < match.home_score:
            count += 1
    return count

def ties(matches: list[Match], team: str) -> int:
    """
    Returns the number of ties for a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate ties for.

    Returns:
        int: The number of ties for the given team.
    """
    count = 0
    for match in matches:
        if match.home_team == team and match.home_score == match.away_score:
            count += 1
        elif match.away_team == team and match.away_score == match.home_score:
            count += 1
    return count

def matches_played(matches: list[Match], team: str) -> int:
    """
    Returns the number of matches played by a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate matches played for.

    Returns:
        int: The number of matches played by the given team.
    """
    count = 0
    for match in matches:
        if match.home_team == team or match.away_team == team:
            count += 1
    return count

def goals_for(matches: list[Match], team: str) -> int:
    """
    Returns the number of goals scored by a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate goals for.

    Returns:
        int: The number of goals scored by the given team.
    """
    count = 0
    for match in matches:
        if match.home_team == team:
            count += match.home_score
        elif match.away_team == team:
            count += match.away_score
    return count

def goals_against(matches: list[Match], team: str) -> int:
    """
    Returns the number of goals conceded by a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate goals against for.

    Returns:
        int: The number of goals conceded by the given team.
    """
    count = 0
    for match in matches:
        if match.home_team == team:
            count += match.away_score
        elif match.away_team == team:
            count += match.home_score
    return count

def record(matches: list[Match], team: str) -> str:
    """
    Returns the record of a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate the record for.

    Returns:
        str: The record of the given
    """
    return f"{wins(matches, team)}-{losses(matches, team)}-{ties(matches, team)}"

def goal_differential(matches: list[Match], team: str) -> int:
    """
    Returns the goal differential for a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate the goal differential for.

    Returns:
        int: The goal differential for the given team.
    """
    return goals_for(matches, team) - goals_against(matches, team)

def points(matches: list[Match], team: str) -> int:
    """
    Returns the number of points for a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate points for.

    Returns:
        int: The number of points for the given team.
    """
    return wins(matches, team) * 3 + ties(matches, team)


def wp(matches: list[Match], team: str, number_of_digits: int = 2) -> float:
    """
    Returns the winning percentage for a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate the winning percentage for.
        number_of_digits (int): The number of digits to round to.

    Returns:
        float: The winning percentage for the given team.
    """
    if matches_played(matches, team) == 0:
        return 0.0
    
    return round(wins(matches, team) / matches_played(matches, team), number_of_digits)

def owp(matches: list[Match], team: str, number_of_digits: int = 2) -> float:
    """
    Returns the opponents' winning percentage for a given team in a list of matches.
    
    :param matches: 
    :param team:
    :param number_of_digits: 
    :return: 
    """
    opponents_wp = []

    for match in matches:
        if match.home_team == team:
            opponent = match.away_team
            opponent_matches = [m for m in matches if m.home_team == opponent or m.away_team == opponent]
            opponent_wins = wins(opponent_matches, opponent)
            opponent_losses = losses(opponent_matches, opponent)
            opponent_ties = ties(opponent_matches, opponent)
            opponent_matches_played = matches_played(opponent_matches, opponent)

            # Exclude the match against the given team
            if match.away_team == opponent:
                if match.home_score > match.away_score:
                    opponent_wins -= 1
                elif match.home_score < match.away_score:
                    opponent_losses -= 1
                else:
                    opponent_ties -= 1
                opponent_matches_played -= 1

            if opponent_matches_played > 0:
                opponents_wp.append((opponent_wins + 0.5 * opponent_ties) / opponent_matches_played)

        elif match.away_team == team:
            opponent = match.home_team
            opponent_matches = [m for m in matches if m.home_team == opponent or m.away_team == opponent]
            opponent_wins = wins(opponent_matches, opponent)
            opponent_losses = losses(opponent_matches, opponent)
            opponent_ties = ties(opponent_matches, opponent)
            opponent_matches_played = matches_played(opponent_matches, opponent)

            # Exclude the match against the given team
            if match.home_team == opponent:
                if match.home_score > match.away_score:
                    opponent_wins -= 1
                elif match.home_score < match.away_score:
                    opponent_losses -= 1
                else:
                    opponent_ties -= 1
                opponent_matches_played -= 1

            if opponent_matches_played > 0:
                opponents_wp.append((opponent_wins + 0.5 * opponent_ties) / opponent_matches_played)

    if not opponents_wp:
        return 0.0

    return round(sum(opponents_wp) / len(opponents_wp), number_of_digits)

def oowp(matches: list[Match], team: str, number_of_digits: int = 2) -> float:
    """
    Returns the opponents' opponents' winning percentage for a given team in a list of matches.
    
    :param matches: 
    :param team:
    :param number_of_digits: 
    :return: 
    """
    opponents_owp = []

    for match in matches:
        if match.home_team == team:
            opponent = match.away_team
        elif match.away_team == team:
            opponent = match.home_team
        else:
            continue

        opponents_owp.append(owp(matches, opponent))

    if not opponents_owp:
        return 0.0

    return round(sum(opponents_owp) / len(opponents_owp), number_of_digits)

def rpi(matches: list[Match], team: str, number_of_digits: int = 2) -> float:
    """
    Returns the Rating Percentage Index (RPI) for a given team in a list of matches.
    
    :param matches: 
    :param team:
    :param number_of_digits: 
    :return: 
    """
    team_wp = wp(matches, team, number_of_digits)
    team_owp = owp(matches, team, number_of_digits)
    team_oowp = oowp(matches, team, number_of_digits)

    return round(0.25 * team_wp + 0.50 * team_owp + 0.25 * team_oowp, number_of_digits)

def goals_per_match(matches: list[Match], team: str) -> float:
    """
    Returns the average number of goals scored per match by a given team in a list of matches.

    Parameters:
        matches (list[Match]): A list of Match objects.
        team (str): The team to calculate the average number of goals scored per match for.

    Returns:
        float: The average number of goals scored per match by the given team.
    """
    if matches_played(matches, team) == 0:
        return 0.0

    return round(goals_for(matches, team) / matches_played(matches, team), 2)
