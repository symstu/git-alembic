from git import Repo
import os

from sqlalchemy import create_engine

from alembic.runtime.migration import MigrationContext, MigrationInfo
from alembic.script import ScriptDirectory, Script
from alembic.config import Config
from alembic import command

from models.history import VersionHistory


class AlembicMigrations:
    def __init__(self):

        self.engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost:5432/alembic")
        self.conn = self.engine.connect()

        self.context = MigrationContext.configure(self.conn)
        self.config = Config('alembic.ini')

        if not os.path.exists('alembic'):
            self.init()

        self.script = ScriptDirectory.from_config(self.config)
        self.git = Repo('')

    def current(self, verbose=False):

        if verbose:
            return command.current(self.config, verbose=True)

        return self.context.get_current_revision()

    def init(self):
        command.init(self.config, 'alembic/', '')

    @property
    def heads(self, verbose=False):

        if verbose:
            command.heads(self.config, verbose=True)

        for head in self.script.get_heads():
            yield self.get_revision(head)

    def get_revision(self, revision_id='9c26830e16a1'):
        return self.script.get_revision(revision_id)

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

            git_branch = self.__get_git_branch__()
            self.config.__setattr__('git_branch', git_branch)

            command.revision(self.config, name)

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

    def __get_branch_name__(self, revision):

        branch = revision.revision

        if hasattr(revision.module, 'git_branch'):
            branch = revision.module.git_branch

        return branch

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

                rev_1_branch = self.__get_branch_name__(rev_1)
                rev_2_branch = self.__get_branch_name__(rev_2)

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

        current_revision = self.current()
        command.upgrade(self.config, rev_heads[0].revision)

        db_log = VersionHistory(current_revision, rev_heads[0].revision)
        db_log.save()

        return True
