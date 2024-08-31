# scaffold.py

import os
import shutil
import click
from jinja2 import Environment, FileSystemLoader

@click.group()
def cli():
    pass

def create_library_files(library_name):
    base_path = os.path.join('libs', library_name)
    os.makedirs(base_path, exist_ok=True)

    template_dir = os.path.join('tools', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))

    templates = {
        'Makefile': 'Makefile',
        'README.md': 'README.md',
        'pyproject.toml': 'pyproject.toml',
        'requirements.txt': 'requirements.txt',
        '.github/workflows/ci.yml': os.path.join('..', '..', '.github', 'workflows', f'ci_{library_name}.yml'),
        'tests/test_example.py': os.path.join('tests', 'test_example.py'),
    }

    context = {
        'library_name': library_name
    }

    for template_name, output_name in templates.items():
        template = env.get_template(template_name)
        output_path = os.path.join(base_path, output_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(template.render(context))

    os.system(
        f'pushd {base_path} && python3 -m venv .venv && source .venv/bin/activate && pip install -r $(git rev-parse --show-toplevel)/pip-requirements.txt && pip install -r $(git rev-parse --show-toplevel)/dev-requirements.txt -r requirements.txt && popd')

def delete_library_files(library_name):
    base_path = os.path.join('libs', library_name)
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    workflow_path = os.path.join('.github', 'workflows', f'ci_{library_name}.yml')
    if os.path.exists(workflow_path):
        os.remove(workflow_path)

@click.command()
@click.argument('library_name')
def create_library(library_name):
    create_library_files(library_name)

@click.command()
@click.argument('library_names', nargs=-1)
def create_libraries(library_names):
    for library_name in library_names:
        create_library_files(library_name)

@click.command()
@click.argument('library_name')
def delete_library(library_name):
    delete_library_files(library_name)

@click.command()
@click.argument('library_names', nargs=-1)
def delete_libraries(library_names):
    for library_name in library_names:
        delete_library_files(library_name)

cli.add_command(create_library)
cli.add_command(create_libraries)
cli.add_command(delete_library)
cli.add_command(delete_libraries)

if __name__ == '__main__':
    cli()