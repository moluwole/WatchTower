"""
@author: Oluwole Majiyagbe
@email: oluwole564@gmail.com

Functionality
=======================
Create the tower tables and columns

Revision ID: d1ec37cb8bce
Revises: 
Create Date: 2019-06-27 10:14:30.297742

"""
from alembic import op
from sqlalchemy import *

from core.utils import uuid

# revision identifiers, used by Alembic.
revision = 'd1ec37cb8bce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('logs',
                    Column('id', INTEGER, primary_key=True, nullable=False, autoincrement=True),
                    Column('clientIp', VARCHAR(length=20)),
                    Column('service', VARCHAR(length=250)),
                    Column('dateOccurred', TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
                    Column('errorMessage', TEXT),
                    Column('stackTrace', TEXT),
                    Column('numberRange', INTEGER),
                    Column('dateAdded', TIMESTAMP(), nullable=False, server_default=text('CURRENT_TIMESTAMP')),
                    Column('dateUpdated', TIMESTAMP(), nullable=False, server_onupdate=text('CURRENT_TIMESTAMP'),
                           server_default=text('CURRENT_TIMESTAMP')))


def downgrade():
    op.drop_table('logs')
