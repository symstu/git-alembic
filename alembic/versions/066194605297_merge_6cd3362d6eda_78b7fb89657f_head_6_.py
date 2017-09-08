""" merge_6cd3362d6eda -> 78b7fb89657f (head), 6({'localization', 'master'})_into_545903c5a54b -> d8855088a719 (head), 9({'develop', 'master'})

Revision ID: 066194605297
Revises: 78b7fb89657f, d8855088a719
Create Date: 2017-09-08 14:41:31.792714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '066194605297'
down_revision = ('78b7fb89657f', 'd8855088a719')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
