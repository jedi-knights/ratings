import click

from .tgs import get_match_results_by_division

@click.group()
def cli():
    pass

@click.command()
@click.option('-g', '--gender', type=click.Choice(['girls', 'boys']), help='Specify the gender for the matches.')
@click.option('-y', '--year', type=click.Choice(['07', '08', '09', '10']), help='Specify the year for the matches.')
def matches(gender: str, year: str):
    click.echo(f'Gender selected: {gender}')
    click.echo(f'Year selected: {year}')

    if gender == 'girls':
        division = f'G20{year}'
    else:
        division = f'B20{year}'

    click.echo(f'Division: {division}')

    # Todo: Retrieve only the matches with the specified division.


cli.add_command(matches)

if __name__ == '__main__':
    cli()
