import os

from git import Repo

from sqlalchemy import create_engine

from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from alembic.config import Config
from alembic import command, util

from faq_migrations.settings import config
from faq_migrations.models import db_session
from faq_migrations.models.history import VersionHistory


class LowLevelApi:

    def __init__(self):
        """
        Load necessary alembic objects such ans Script and Context
        """

        if not config.alembic_dir:
            raise ValueError('Please setup config.alembic_dir param')

        # loading alembic.ini config from installed path
        self.init_config = Config(config.alembic_dir + 'alembic.ini')

        # create database connection
        self.engine = create_engine(self.__database_url__)
        self.conn = self.engine.connect()

        # and load Alembic Context
        self.context = MigrationContext.configure(self.conn)

    @property
    def script(self):
        """
        Get ScripDirectory

        :return: ScripDirectory Object based on config.alembic_dir
        """

        if not os.path.exists(config.alembic_dir):
            raise Exception('Dir {} not found'.format(config.alembic_dir))

        return ScriptDirectory.from_config(self.init_config)

    @property
    def __database_url__(self):
        """
        Get DatabaseUrl
        example: postgresql+psycopg2://postgres:postgres@localhost:5432/alembic

        :return: database url
        """
        return config.database_url or self.init_config.get_section_option(
            'alembic', 'sqlalchemy.url'
        )

    @__database_url__.setter
    def __database_url__(self, db_url):
        """
        Set sqlalchemy.url in alembic.ini

        :param db_url: database url
        """
        self.init_config.set_section_option(
            'alembic', 'sqlalchemy.url', db_url
        )

    def __get_last_revision__(self):
        """
        Get last revision

        :return: revision object ot None if migration does not exist
        """

        revisions = [revision for revision in self.script.walk_revisions()]

        if revisions:

            if len(revisions) == 1:
                return revisions[0]

            return revisions[:-1][0]

        return None

    @staticmethod
    def __get_git_branch__():
        """
        Get current git branch

        :return: current git branch
        """
        return str(Repo('').active_branch)

    def __set_branch_to_script__(self):
        """
        Write into migration current git branch name
        """
        self.init_config.__setattr__('git_branch', self.__get_git_branch__())

    @staticmethod
    def __merge_choices__(revision_heads):
        """
        Return merge choices of merge sequence

        :param revision_heads: name of heads
        :return: list of available merges
        """

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

    @staticmethod
    def __branch_name__(revision):
        """
        Git branch name of specific migration (Revision)

        :param revision: Revision object (migration)
        :return: git branch name
        """

        branch = revision.revision

        if hasattr(revision.module, 'git_branch'):
            branch = revision.module.git_branch

        return branch


class AlembicMigrations(LowLevelApi):
    """
    Class-Wrapper for Alembic that implement some functionality from Alembic
    """

    def __init__(self):

        super(AlembicMigrations, self).__init__()
        self.__set_branch_to_script__()

    @staticmethod
    def init():
        """
        Prepare directory with alembic.ini, mako-files and directory for
        migrations. Part of functional was copied from original Alembic Init
        but changed some things with config
        """
        if os.access(config.alembic_dir, os.F_OK):
            raise util.CommandError(
                "Directory {} already exists".format(config.alembic_dir)
            )

        template_dir = os.path.join(
            config.template_path + config.template_name
        )

        if not os.access(template_dir, os.F_OK):
            raise util.CommandError("No such template {}".format(template_dir))

        util.status(
            "Creating directory {}".format(
                os.path.abspath(config.alembic_dir)
            ), os.makedirs, config.alembic_dir
        )

        versions = os.path.join(config.alembic_dir, 'versions')
        util.status("Creating directory %s" % os.path.abspath(versions),
                    os.makedirs, versions)

        script = ScriptDirectory(config.alembic_dir)

        dirs = os.listdir(template_dir)
        dirs += ['versions/create_table_alembic_version_history.py', ]

        for file_ in dirs:
            file_path = os.path.join(template_dir, file_)

            if file_ == 'alembic.ini.mako':
                config_file = os.path.abspath('alembic.ini')
                if os.access(config_file, os.F_OK):
                    util.msg("File {} already exists, skipping".format(
                        config_file)
                    )
                else:
                    script._generate_template(
                        template_dir + '/alembic.ini.mako',
                        os.path.join(config.alembic_dir, 'alembic.ini'),
                        script_location=config.alembic_dir
                    )
            elif os.path.isfile(file_path):
                output_file = os.path.join(config.alembic_dir, file_)
                script._copy_file(
                    file_path,
                    output_file
                )

        util.msg("Please edit configuration/connection/logging "
                 "settings in {} before proceeding.".format(
            os.path.join(config.alembic_dir, 'alembic.ini'))
        )

    def current(self, verbose=False):
        """
        Return hottest Revision Object

        :param verbose: additional information
        :return: last Revision Object
        """

        if verbose:
            return command.current(self.init_config, verbose=True)

        return self.context.get_current_revision()

    @property
    def heads(self, verbose=False):
        """
        Get heads

        :param verbose: additional information
        :return: Head Revisions
        """
        if verbose:
            command.heads(self.init_config, verbose=True)

        for head in self.script.get_heads():
            yield self.get_revision(head)

    def get_revision(self, revision_id='9c26830e16a1'):
        """
        Get Revision by ID

        :param revision_id: id of revision, parameter `revision` in migration
        :return: Revision Object with specific id
        """
        return self.script.get_revision(revision_id)

    def create(self, name):
        """
        Create new migration, but if exists more then one head you must
        merge it firstly

        :param name: name of new migration
        """

        r_heads = [head for head in self.heads]

        if len(r_heads) < 2:
            command.revision(self.init_config, name)

        else:
            util.msg('There are {} heads.\n'
                     'You must merge migrations first.'.format(len(r_heads)))
            self.merge()

    def merge(self):
        """
        Perform merging of migrations if exists more then one head
        """
        revision_heads = [head for head in self.heads]

        if len(revision_heads) < 2:
            util.msg('There are not migrations for merge')
        else:
            print('\n\n-------------------------------------------------')
            merge_choices = [choice for choice in
                             self.__merge_choices__(revision_heads)]
            for choice in merge_choices:

                rev_1 = choice['migration1']
                rev_2 = choice['migration2']

                rev_1_branch = self.__branch_name__(rev_1)
                rev_2_branch = self.__branch_name__(rev_2)

                util.msg('{}) {}:{} -> {}:{}'.format(
                    choice["inc"], rev_1_branch, rev_1, rev_2_branch, rev_2
                ))

            util.msg('-------------------------------------------------\n\n')

            choice = input('Choose migration:\n')

            try:
                choice = int(choice)

                if not (1 <= choice <= len(merge_choices)):
                    util.msg('Input value must be between 1 and {}'.format(
                        len(merge_choices))
                    )
                    exit(0)

                rev_1 = merge_choices[choice - 1]['migration1']
                rev_2 = merge_choices[choice - 1]['migration2']

                command.merge(
                    self.init_config,
                    revisions=[rev_2.revision, rev_1.revision],
                    message='merge_{}({})_into_{}({})'.format(
                        rev_1, rev_1.branch_labels, rev_2, rev_2.branch_labels
                    )
                )

            except ValueError:
                util.msg('Your choice must be of int data type')

    def history(self, limit=10, upper=True):
        """
        Show migrations

        :param limit: limit of output migrations
        :param upper: sorting. True - new at the top

        :return: Revision objects
        """

        revisions = [revision for revision in self.script.walk_revisions()]

        if limit < len(revisions):
            limit = len(revisions)

        if upper:
            return revisions[-limit:]

        return revisions[0: limit]

    def migrate(self):
        """
        Perform upgrading of your database

        :return: True if OK
        """

        rev_heads = [head for head in self.heads]

        if len(rev_heads) > 1:
            return False

        upgrade_migrations = self.upgrade_revisions(rev_heads[0].revision)

        util.msg('upgrade_migrations: {}'.format(upgrade_migrations))

        if not len(upgrade_migrations):
            raise Exception('There are not new migrations')

        for migration in upgrade_migrations:
            command.upgrade(self.init_config, migration.revision)

            # it may be a list when revision in merge point
            down_revision = str(migration.down_revision)
            util.msg('migrating from `{}` to {}'.format(
                down_revision, migration.revision)
            )

            # initial migration
            if not down_revision:
                util.msg('current_revision: {}'.format(down_revision))
                continue

            db_log = VersionHistory(down_revision, migration.revision)
            util.msg('saved migration: ', db_log.save())

        return True

    def upgrade_revisions(self, head):
        """
        Return list of migrations that will be done

        :param head: current head
        :return: Revision Objects
        """
        revisions = self.script.iterate_revisions(head, self.current())
        return [rev for rev in revisions][::-1]

    @property
    def all_local_revisions(self):
        """
        List of all created migrations
        :return: Revision Objects
        """
        return [rev for rev in self.script.walk_revisions()][::-1]

    def branch_name(self, revision):
        """
        Get Git Branch Name from migration file by revision id

        :param revision: if of revision
        :return: git branch name of specific revision
        """
        return self.__branch_name__(revision)


class CompareLocalRemote:
    """
    This is a util that verify migration sequence of created local file and
    alembic_version_history in database
    """

    def __init__(self):
        self.session = AlembicMigrations()

    def compare_history(self):
        """
        Compare local migrations sequence and remote at the database. Raise
        Exception if local and remote sequence are not same.
        """
        engine = self.session.engine

        if not engine.dialect.has_table(engine, VersionHistory):
            raise Exception('Table `alembic_version_history` does not exists,'
                            ' please migrate your db first')

        remote_history = db_session.query(VersionHistory) \
            .order_by(VersionHistory.id.asc()) \
            .all()
        local_history = self.session.all_local_revisions

        for index, remote_revision in enumerate(remote_history):
            print('{}| remote <{}> : local {}'.format(
                index, remote_revision, local_history[index].revision
            ))

            if str(remote_revision.previous_revision) != \
                    str(local_history[index].down_revision):
                previous = remote_revision.previous_revision
                down_revision = local_history[index].down_revision

                raise Exception('Down revision is incorrect: remote `{}` != '
                                'local `{}`'.format(previous, down_revision))

            if str(remote_revision.forward_revision) != \
                    str(local_history[index].revision):
                raise Exception('Forward revision is incorrect')
