from git import Repo

from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

from alembic.script import ScriptDirectory
from alembic.config import Config
from alembic import command

import click


engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/alembic")
conn = engine.connect()

context = MigrationContext.configure(conn)

current_rev = context.get_current_revision()
print('current_rev: ', current_rev)

config = Config('alembic.ini')
script = ScriptDirectory.from_config(config)

# head_revision = script.get_current_head()
heads_revision = script.get_heads()
print('heads: ', heads_revision)

repo = Repo('')
# branch = str(repo.active_branch)
branch = 'develop'
print('branch: ', branch)


def create_migration(message):
    command.revision(config, message)


# @click.command()
# @click.option('--name', default='')
# @click.option('--action', default=None)
# def migrator(action, name):
#
#     print(f'{action}:{name}')
#     print('action type: ', type(action))
#     if str(action) == 'create:':
#
#         print('in create')
#
#     if len(heads_revision) > 2:
#         click.echo(f'Only 2 branches could be merged: {heads_revision}')
#
#     elif len(heads_revision) == 2:
#         command.merge(config, heads_revision, message='AUTO_MERGE',
#                       branch_label=branch)
#         click.echo('Created merge before new migration')
#
#         command.revision(config, name)
#
#     click.echo(f'created new revision for : {name}')
#
#     if action == 'merge':
#
#         if len(heads_revision) > 2:
#             raise KeyError(f'Only 2 branches could be merged: {heads_revision}')
#
#         elif len(heads_revision) == 2:
#             command.merge(config, heads_revision, message='AUTO_MERGE',
#                           branch_label=branch)
#         click.echo('merged')
#
#     elif action == 'history':
#         command.history(config)
#         click.echo('last history')


if __name__ == '__main__':

    # migrator()
    #
    # if len(heads_revision) > 2:
    #     click.echo(f'Only 2 branches could be merged: {heads_revision}')
    #
    # elif len(heads_revision) == 2:
    #     command.merge(config, heads_revision, message='AUTO_MERGE',
    #                   branch_label=branch)
    #     click.echo('Created merge before new migration')

    command.revision(config, '9', head='38b0b18c04a1')
    # command.revision(config, '6', branch_label=branch)
