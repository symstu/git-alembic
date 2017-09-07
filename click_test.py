import click

from git import Repo

from sqlalchemy import create_engine

from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from alembic.config import Config
from alembic import command


class AlembicMigrations:
    def __init__(self):
        self.engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost:5432/alembic")
        self.conn = self.engine.connect()

        self.context = MigrationContext.configure(self.conn)
        self.config = Config('alembic.ini')
        self.script = ScriptDirectory.from_config(self.config)
        self.git = Repo('')

    def current(self, verbose=False):

        if verbose:
            return command.current(self.config, verbose=True)

        return self.context.get_current_revision()

    def heads(self, verbose=False):

        if verbose:
            command.heads(self.config, verbose=True)

        return self.script.get_heads()

    def get_revision(self, revision_id='cc4c3a879191'):
        rev = self.script.get_revision(revision_id)
        print(rev)

    def __get_git_branch__(self):
        return str(self.git.active_branch)

    def create(self, name):
        r_heads = self.heads()
        print(r_heads)

        if len(r_heads) == 1:
            print('one head')
            command.revision(self.config, name,
                             branch_label=self.__get_git_branch__())
        else:
            print(f'There are {len(r_heads)} heads: {r_heads}.\n'
                  f'You must merge migrations first.')

    def merge(self):
        r_heads = self.heads()

        if len(r_heads) < 2:
            print('There are not migrations for merge')
        else:
            print('\n\n-------------------------------------------------')
            choices = []
            inc = 0

            for rev_1 in r_heads:
                for rev_2 in r_heads:
                    if rev_1 != rev_2:

                        inc += 1

                        _rev_1 = self.script.get_revision(rev_1)
                        _rev_2 = self.script.get_revision(rev_2)

                        choices.append(
                            dict(
                                migration1=_rev_1,
                                migration2=_rev_2
                            )
                        )
                        print(f'{inc}) {_rev_1.branch_labels} -> '
                              f'{_rev_2.branch_labels}')

            print('-------------------------------------------------\n\n')

            choice = input('Choose migration:\n')

            try:
                choice = int(choice)

                if not (1 <= choice <= inc):
                    print(f'Input value must be between 1 and {inc}')
                    exit(0)

                rev_1 = choices[choice - 1]['migration1'].revision
                rev_2 = choices[choice - 1]['migration2'].revision

                # print('choosen: ', choices[choice - 1])
                # print(f'{rev_1.branch_labels} -> {rev_2.branch_labels}')

                command.merge(
                    self.config,
                    revisions=[rev_1.revision, rev_2.revision],
                    message=f'merge_{rev_1.revision}_into_{rev_2.revision}'
                )

            except ValueError:
                print('Your choice must be of int data type')


al = AlembicMigrations()


@click.group()
def cli():
    pass


@cli.command()
# @click.argument('name')
def heads():
    print(al.heads())


@cli.command()
# @click.argument('name', default='hui')
def current():
    print(al.current(True))


@cli.command()
@click.argument('name')
def create(name):
    print(al.create(name))


@cli.command()
def merge():
    al.merge()


@cli.command()
def revision_ver():
    al.get_revision()

if __name__ == '__main__':
    cli()
