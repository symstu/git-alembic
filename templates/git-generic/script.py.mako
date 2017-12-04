"""

${message}

Create Date: ${create_date}

"""


# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}
git_branch = ${repr(config.git_branch)}

# importing happify project root
import sys
sys.path.insert(0, "..")


from alembic.op import (add_column, create_foreign_key, create_table,
                        drop_constraint, create_unique_constraint,
                        create_index, drop_index, alter_column,
                        drop_column, drop_table, execute, get_bind, rename_table)
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSON


# Example usage
# =====================
# create_table(
#     'table_name',
#     Column('id', Integer, primary_key=True),
#     Column('user_id', Integer, nullable=False, index=True),
#     Column('title', String),
#     Column('created_at', DateTime, index=True, server_default=text('now()')),
#     Column('updated_at', DateTime, index=True, server_default=text('now()'), server_onupdate=text('now()')),
# )
#
# add_column('a_table_name', Column('technique_id', Integer, nullable=True))
#
# alter_column(
#     table_name, column_name, nullable=None, server_default=False, new_column_name=None,
#     type_=None, existing_type=None, existing_server_default=False, existing_nullable=None, schema=None
# )
#
# Foreign Key (2 versions)
# =============
# create_foreign_key(
#     'fk_constraint_name',
#     from_table, to_table,
#     ['from_column'], ['to_column']
# )
#
# add_column('a_table_name', Column('technique_id', Integer, ForeignKey('model.property'), nullable=True))
# =============
#
# Create Index (2 versions)
# =============
# create_index('index_name', 'table_name', ['columns',])
#
# add_column('a_table_name', Column('technique_id', Integer, nullable=True, index=True))
# =============
#
# rename_table('old_table_name', 'new_table_name')
#
# drop_constraint('fk_boards_users', 'boards')
#
# drop_index('index_name')
#
# drop_column('pins', 'page_url')
#
# drop_table('boards')
#
# =====================


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    pass
