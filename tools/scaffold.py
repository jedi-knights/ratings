# scaffold.py

import os
import click

from jinja2 import Environment, FileSystemLoader

@click.group()
def cli():
    pass


@click.command()
@click.argument('library_name')
def create_library(library_name):
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


cli.add_command(create_library)

if __name__ == '__main__':
    cli()
