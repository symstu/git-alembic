""" merge_abf6b43bfeb8 -> c2c97da30222 (head), 7({'master'})_into_68d1e2be532c -> b1749afbc04f (head), 4({'master', 'develop'})

Revision ID: 91e3b5d1dd8e
Revises: c2c97da30222, b1749afbc04f
Create Date: 2017-09-08 14:10:58.835615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91e3b5d1dd8e'
down_revision = ('c2c97da30222', 'b1749afbc04f')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
