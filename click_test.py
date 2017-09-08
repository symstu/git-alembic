import click

from git import Repo

from sqlalchemy import create_engine

from alembic.runtime.migration import MigrationContext, MigrationInfo
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

    @property
    def heads(self, verbose=False):

        if verbose:
            command.heads(self.config, verbose=True)

        for head in self.script.get_heads():
            yield self.get_revision(head)

    def get_revision(self, revision_id='9c26830e16a1'):
        rev = self.script.get_revision(revision_id)
        return rev

    def __get_last_revision__(self):

        revisions = [revision for revision in self.script.walk_revisions()]

        if revisions:

            if len(revisions) == 1:
                return revisions[0]

            return revisions[:-1][0]

        return None

    def __get_git_branch__(self):
        return str(self.git.active_branch)

    def create(self, name):

        r_heads = [head for head in self.heads]

        if len(r_heads) < 2:

            rev = self.__get_last_revision__()
            git_branch = self.__get_git_branch__()

            # Initial revision, set up current branch label
            if not rev:
                command.revision(self.config, name, branch_label=git_branch)
                return

            # Continues revision - same branch name OR
            # if it was merged
            if (rev and (git_branch in rev.branch_labels)) or \
                    (len(rev.down_revision) > 1):
                command.revision(self.config, name)
                return

            # Branch has changed - new branch label
            command.revision(self.config, name, branch_label=git_branch)

        else:
            print(f'There are {len(r_heads)} heads.\n'
                  f'You must merge migrations first.')
            self.merge()

    @staticmethod
    def __merge_choices__(revision_heads):

        inc = 0

        for rev_1 in revision_heads:
            for rev_2 in revision_heads:
                if rev_1 != rev_2:

                    inc += 1

                    yield dict(
                        inc=inc,
                        migration1=rev_1,
                        migration2=rev_2
                    )

    def merge(self):
        revision_heads = [head for head in self.heads]

        if len(revision_heads) < 2:
            print('There are not migrations for merge')
        else:
            print('\n\n-------------------------------------------------')
            merge_choices = [choice for choice in
                             self.__merge_choices__(revision_heads)]
            for choice in merge_choices:

                rev_1 = choice['migration1']
                rev_2 = choice['migration2']

                rev_1_branch = set(rev_1.branch_labels)
                rev_2_branch = set(rev_2.branch_labels)

                print(f'{choice["inc"]}) {rev_1_branch} -> '
                      f'{rev_2_branch}')

            print('-------------------------------------------------\n\n')

            choice = input('Choose migration:\n')

            try:
                choice = int(choice)

                if not (1 <= choice <= len(merge_choices)):
                    print(f'Input value must be between 1 and '
                          f'{len(merge_choices)}')
                    exit(0)

                rev_1 = merge_choices[choice - 1]['migration1']
                rev_2 = merge_choices[choice - 1]['migration2']

                command.merge(
                    self.config,
                    revisions=[rev_2.revision, rev_1.revision],
                    message=f'merge_{rev_1}({rev_1.branch_labels})_into_{rev_2}'
                            f'({rev_2.branch_labels})'
                )

            except ValueError:
                print('Your choice must be of int data type')

    def history(self, limit=10, upper=True):

        revisions = [revision for revision in self.script.walk_revisions()]

        if limit < len(revisions):
            limit = len(revisions)

        if upper:
            return revisions[-limit:]

        return revisions[0: limit]

    def migrate(self):

        rev_heads = [head for head in self.heads]

        if len(rev_heads) > 1:
            return False

        command.upgrade(self.config, rev_heads[0].revision)

        return True

al = AlembicMigrations()


@click.group()
def cli():
    pass


@cli.command()
def heads():

    print('------------------------------------------')

    for head in al.heads:
        print(f'{head.longdoc}')
        print(f'Branch labels: {head.branch_labels}')
        print('------------------------------------------')


@cli.command()
def current():
    print(al.current(True))


@cli.command()
@click.argument('name')
def create(name):
    al.create(name)


@cli.command()
def merge():
    al.merge()


@cli.command()
def last_revision():
    print(al.__get_last_revision__())


@cli.command()
def revision_ver():
    al.get_revision()


@cli.command()
def migrate():
    if not al.migrate():
        print('\nYou must merge branches first\n')
        al.merge()


@cli.command()
@click.argument('limit', default=10)
def history(limit, upper=True):

    revisions = al.history(limit, upper)

    for revision in revisions:
        print(f'{revision} {revision.branch_labels}')


if __name__ == '__main__':
    cli()
