"""
Command Line modules. Some code command line to use in creating templates and running the app

@author: OLuwole Majiyagbe
@contact: oluwole.majiyagbe@firstpavitech.com
@organization: First Pavilion
"""

import os
import shutil
import click
import re
from subprocess import call
from base64 import b64encode
from colorama import init, Fore, Back

from core.utils import camelcase_to_underscore, string_to_class_name_format, clean_file_name

SERVER_PATH = os.path.abspath('.')
__version__ = 0.1


def get_details(file_name):
    name = click.prompt(Fore.CYAN + "Your name ")
    email = click.prompt(Fore.CYAN + "Email ")
    organization = "First Pavilion"
    controller_use = click.prompt(Fore.CYAN + "Why do we need another {}? ".format(file_name))
    return name, email, organization, controller_use


@click.group()
@click.version_option(__version__)
def main():
    init(autoreset=True)
    pass


@main.command('create:controller', short_help="Create Controller File")
@click.argument('filename')
def create_controller(filename):
    """Name of the controller file to be created"""
    path = '{}/controllers'.format(SERVER_PATH)
    if not os.path.exists(path):
        os.makedirs(path)

    file_name = str(clean_file_name(filename) + '.py')
    if os.path.isfile(path + "/" + file_name):
        click.echo(Fore.WHITE + Back.RED + "ERROR: Controller file exists")
        return

    name, email, org, usage = get_details("controller")
    controller_file = open(os.path.abspath('.') + '/controllers/' + file_name, 'w+')

    compose = '"""\n{0}\n@author: {1}\n@email: {2}\n@organisation: {3}\n"""'.format(usage, name, email, org)

    controller_file.write(compose)
    controller_file.close()
    click.echo(Fore.GREEN + "Controller " + filename + " created successfully")


@main.command('create:model', short_help="Create Model File")
@click.argument('tablecolumn', required=1)
def create_model(tablecolumn):
    """Model name"""
    path = '{}/models'.format(SERVER_PATH)
    if not os.path.exists(path):
        os.makedirs(path)

    table_name = camelcase_to_underscore(tablecolumn)
    file_name = str(clean_file_name(table_name) + '.py')
    if os.path.isfile(path + "/" + file_name):
        click.echo(Fore.WHITE + Back.RED + "ERROR: Model file exists")
        return
    name, email, org, usage = get_details("model")
    model_file = open(os.path.abspath('.') + '/models/' + file_name, 'w+')
    class_name = string_to_class_name_format(tablecolumn)

    compose = '"""\n{0}\n@author: {1}\n@email: {2}\n@organisation: {3}\n"""\n\n'.format(usage, name, email, org)

    sqlalchemy_imports = 'from sqlalchemy import *\nfrom core import db\nfrom core.utils import uuid\n\n\nclass {0}(' \
                         'db.OurMixin, db.Base):\n    __tablename__ = \'{1}\''.format(class_name, table_name)
    compose += sqlalchemy_imports

    model_file.write(str(compose))
    model_file.close()
    click.echo(Fore.GREEN + "Model " + file_name + " created")


@main.command('run', short_help="Run the App")
def run():
    """Run the service in the console"""
    
