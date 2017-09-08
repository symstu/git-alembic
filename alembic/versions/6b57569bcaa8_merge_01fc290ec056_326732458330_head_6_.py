""" merge_01fc290ec056 -> 326732458330 (head), 6({'localization', 'master'})_into_bc06534b665b, 45825a717529 -> 897f8fb2f539 (head) (mergepoint), merge_ea9f40881640 -> 45825a717529 (head), 7({'master'})_into_943d01cec8db -> bc06534b665b (head), 4({'develop', 'master'})({'master', 'develop'})

Revision ID: 6b57569bcaa8
Revises: 897f8fb2f539, 326732458330
Create Date: 2017-09-08 16:31:35.202060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b57569bcaa8'
down_revision = ('897f8fb2f539', '326732458330')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
