""" merge_ea9f40881640 -> 45825a717529 (head), 7({'master'})_into_943d01cec8db -> bc06534b665b (head), 4({'develop', 'master'})

Revision ID: 897f8fb2f539
Revises: bc06534b665b, 45825a717529
Create Date: 2017-09-08 16:25:51.557563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '897f8fb2f539'
down_revision = ('bc06534b665b', '45825a717529')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
