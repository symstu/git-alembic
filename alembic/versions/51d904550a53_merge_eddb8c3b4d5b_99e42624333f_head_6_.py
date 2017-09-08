""" merge_eddb8c3b4d5b -> 99e42624333f (head), 6({'master', 'localization'})_into_b7e333fdf2ff, 27d4b671a7ac -> 49141f0f4cab (head) (mergepoint), merge_f0b6a3420e18 -> 27d4b671a7ac (head), 7({'master'})_into_661f55e88801 -> b7e333fdf2ff (head), 4({'master', 'develop'})({'develop', 'master'})

Revision ID: 51d904550a53
Revises: 49141f0f4cab, 99e42624333f
Create Date: 2017-09-08 15:21:02.798434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51d904550a53'
down_revision = ('49141f0f4cab', '99e42624333f')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
