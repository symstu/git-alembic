""" merge_f0b6a3420e18 -> 27d4b671a7ac (head), 7({'master'})_into_661f55e88801 -> b7e333fdf2ff (head), 4({'master', 'develop'})

Revision ID: 49141f0f4cab
Revises: b7e333fdf2ff, 27d4b671a7ac
Create Date: 2017-09-08 15:17:53.475629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49141f0f4cab'
down_revision = ('b7e333fdf2ff', '27d4b671a7ac')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
