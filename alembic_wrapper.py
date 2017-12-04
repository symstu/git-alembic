from git import Repo
import os

from sqlalchemy import create_engine

from alembic.runtime.migration import MigrationContext, MigrationInfo
from alembic.script import ScriptDirectory, Script
from alembic.config import Config
from alembic import command, util

from models.history import VersionHistory


class AlembicMigrations:
    def __init__(self):

        self.engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost:5432/alembic")
        self.conn = self.engine.connect()

        self.context = MigrationContext.configure(self.conn)
        self.config = Config('alembic.ini')

        if os.path.exists('alembic'):
            # self.init()
            self.script = ScriptDirectory.from_config(self.config)

    def current(self, verbose=False):

        if verbose:
            return command.current(self.config, verbose=True)

        return self.context.get_current_revision()

    @staticmethod
    def init(directory='alembic', template='git-generic'):

        if os.access(directory, os.F_OK):
            raise util.CommandError("Directory %s already exists" % directory)

        template_dir = os.path.join('templates/',
                                    template)
        if not os.access(template_dir, os.F_OK):
            raise util.CommandError("No such template %r" % template)

        util.status("Creating directory %s" % os.path.abspath(directory),
                    os.makedirs, directory)

        versions = os.path.join(directory, 'versions')
        util.status("Creating directory %s" % os.path.abspath(versions),
                    os.makedirs, versions)

        script = ScriptDirectory(directory)

        dirs = os.listdir(template_dir)
        dirs += ['versions/create_table_alembic_version_history.py', ]

        for file_ in dirs:
            file_path = os.path.join(template_dir, file_)

            if file_ == 'alembic.ini.mako':
                config_file = os.path.abspath('alembic.ini')
                if os.access(config_file, os.F_OK):
                    util.msg("File %s already exists, skipping" % config_file)
                else:
                    script._generate_template(
                        file_path,
                        config_file,
                        script_location=directory
                    )
            elif os.path.isfile(file_path):
                output_file = os.path.join(directory, file_)
                script._copy_file(
                    file_path,
                    output_file
                )

        util.msg("Please edit configuration/connection/logging "
                 "settings in %r before proceeding." % config_file)

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

    @staticmethod
    def __get_git_branch__():
        return str(Repo('').active_branch)

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

    def branch_name(self, revision):

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

                rev_1_branch = self.branch_name(rev_1)
                rev_2_branch = self.branch_name(rev_2)

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

        upgrade_migrations = self.upgrade_revisions(rev_heads[0].revision)

        print(f'upgrade_migrations: {upgrade_migrations}')

        if not len(upgrade_migrations):
            raise Exception('There are not new migrations')

        for migration in upgrade_migrations:
            command.upgrade(self.config, migration.revision)
            print(f'migrating from `{migration.down_revision}` to '
                  f'{migration.revision}')

            # initial migration
            if not migration.down_revision:
                print('current_revision: ', migration.down_revision)
                continue

            db_log = VersionHistory(migration.down_revision, migration.revision)
            print('saved migration: ', db_log.save())

        return True

    def upgrade_revisions(self, head):
        return [rev for rev in self.script.iterate_revisions(head, self.current())][::-1]
