"""
@author: Oluwole Majiyagbe
@email: oluwole.majiyagbe@firstpavitech.com
@organisation: First Pavilion

Functionality
=======================
Create the watcher tables and columns

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
                    Column(u'id', CHAR(length=36), default=uuid, primary_key=True, nullable=False),
                    Column(u'clientIp', VARCHAR(length=20)),
                    Column(u'service', VARCHAR(length=250)),
                    Column(u'dateOccurred', TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
                    Column(u'errorMessage', TEXT),
                    Column(u'stackTrace', TEXT),
                    Column('clientId', CHAR(length=36)),
                    Column('dateAdded', TIMESTAMP(), nullable=False, server_default=text('CURRENT_TIMESTAMP')),
                    Column(u'dateUpdated', TIMESTAMP(), nullable=False, server_onupdate=text('CURRENT_TIMESTAMP'),
                           server_default=text('CURRENT_TIMESTAMP')))


def downgrade():
    op.drop_table('logs')
