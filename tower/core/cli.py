"""
Command Line modules. Some code command line to use in creating templates and running the app

@author: Oluwole Majiyagbe
@email: oluwole564@gmail.com
"""

import os
import time
import click
import re
from subprocess import call
from base64 import b64encode
from colorama import init, Fore, Back

from core.utils import camelcase_to_underscore, string_to_class_name_format, clean_file_name

SERVER_PATH = os.path.abspath('.')
__version__ = 0.1


def get_details(command_type):
    name = click.prompt(Fore.CYAN + "Your name ")
    email = click.prompt(Fore.CYAN + "Email ")
    organization = "First Pavilion"
    controller_use = click.prompt(Fore.CYAN + "Why do we need another {0}? ".format(command_type))
    filename = clean_file_name(click.prompt(Fore.CYAN + "Your {0} name".format(command_type)))
    return name, email, organization, controller_use, filename


@click.group()
@click.version_option(__version__)
def main():
    init(autoreset=True)
    pass


@main.command('create:controller', short_help="Create Controller File")
def create_controller():
    """Name of the controller file to be created"""
    path = '{}/controllers'.format(SERVER_PATH)
    if not os.path.exists(path):
        os.makedirs(path)

    name, email, org, usage, file_name = get_details("controller")

    file_name = file_name + ".py"
    if os.path.isfile(path + "/" + file_name):
        click.echo(Fore.WHITE + Back.RED + "ERROR: Controller file exists")
        return

    controller_file = open(os.path.abspath('.') + '/controllers/' + file_name, 'w+')

    compose = '"""\n{0}\n@author: {1}\n@email: {2}\n@organisation: {3}\n"""'.format(usage, name, email, org)

    controller_file.write(compose)
    controller_file.close()
    click.echo(Fore.GREEN + "Controller " + file_name + " created successfully")


@main.command('create:model', short_help="Create Model File")
def create_model():
    """Model name"""
    path = '{}/models'.format(SERVER_PATH)
    if not os.path.exists(path):
        os.makedirs(path)

    name, email, org, usage, tablecolumn = get_details("model")

    table_name = camelcase_to_underscore(tablecolumn)
    file_name = str(clean_file_name(table_name) + '.py')
    if os.path.isfile(path + "/" + file_name):
        click.echo(Fore.WHITE + Back.RED + "ERROR: Controller file exists")
        return

    model_file = open(os.path.abspath('.') + '/models/' + file_name, 'w+')
    class_name = string_to_class_name_format(tablecolumn)

    compose = '"""\n{0}\n@author: {1}\n@email: {2}\n@organisation: {3}\n"""\n\n'.format(usage, name, email, org)

    sqlalchemy_imports = 'from sqlalchemy import *\nfrom core import db\nfrom core.utils import uuid\n\n\nclass {0}(' \
                         'db.OurMixin, db.Base):\n    __tablename__ = \'{1}\''.format(class_name, table_name)
    compose += sqlalchemy_imports

    model_file.write(str(compose))
    model_file.close()
    click.echo(Fore.GREEN + "Model " + file_name + " created")


@main.command('create:migration', short_help="Create a migration File")
def create_migration():
    name, email, org, usage, file_name = get_details("migration")
    migration_path = SERVER_PATH + '/migrations/versions'

    files = os.listdir(migration_path)

    compose = '\n@author: {1}\n@email: {2}\n@organisation: {3}\n\nFunctionality\n=======================\n{0}' \
        .format(usage, name, email, org)

    call(['alembic', '-c', SERVER_PATH + "/migrations/alembic.ini", 'revision', '-m', compose])

    rename = ""
    click.echo(Fore.MAGENTA + "Renaming Migration File")
    time.sleep(5)
    for filename in os.listdir(migration_path):
        if filename not in files:
            rename = "{0}_{1}.py".format(len(files), camelcase_to_underscore(file_name.replace(' ', '_')))
            os.rename(os.path.join(migration_path, filename), os.path.join(migration_path, rename))
            break

    click.echo(Fore.GREEN + "Migration {0} created".format(rename))


@main.command('run:migration', short_help="Run Migrations against the database")
@click.option('-r', '--revision', 'revision', default=None)
def run_migration(revision):
    """Run Migrations"""
    if revision is None:
        call(['alembic', '-c', SERVER_PATH + "/migrations/alembic.ini", 'upgrade', 'head'])
    else:
        call(['alembic', '-c', SERVER_PATH + "/migrations/alembic.ini", 'upgrade', revision])


@main.command('migration:rollback', short_help="Roll Back Migration")
@click.option('-r', '--revision', 'revision', default=None)
def rollback(revision):
    if revision is None:
        if click.confirm('Rollback Last Migration?'):
            call(['alembic', '-c', SERVER_PATH + "/migrations/alembic.ini", 'downgrade', '-1'])
    else:
        if click.confirm('Rollback Migration?'):
            call(['alembic', '-c', SERVER_PATH + "/migrations/alembic.ini", 'downgrade', revision])


@main.command('migration:reset', short_help="Reset Migration")
def reset():
    if click.confirm(Fore.RED + 'Resetting Migrations would clear all data and schemas in Database. Continue?'):
        call(['alembic', '-c', SERVER_PATH + "/migrations/alembic.ini", 'downgrade', 'base'])


@main.command('migration:history', short_help="Show Migration History")
def show_history():
    """Show Migration history"""
    call(['alembic', '-c', SERVER_PATH + "/migrations/alembic.ini", 'history', '--verbose'])


@main.command('run', short_help="Run the App")
def run():
    """Run the service in the console"""
    click.echo(Fore.GREEN + "Running App")
    call(['./app.py'])
