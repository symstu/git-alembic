import click


@click.group(help="Creating of new migrations and upgrading database")
def migrations():
    pass


@migrations.command(help='Initialize new alembic directory')
def init():
    """
    Creates new directory for migrations, generates alembic.ini and mako-files
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations
    AlembicMigrations().init()


@migrations.command(help='Show current heads')
def heads():
    """
    Show current heads
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations

    al = AlembicMigrations()

    print('------------------------------------------')
    for head in al.heads:
        print(head.longdoc)
        print('Branch: {}'.format(al.branch_name(head)))
        print('------------------------------------------')


@migrations.command(help='Show current migration revision')
def current():
    """
    Show current migration revision from database
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations
    print(AlembicMigrations().current(True))


@migrations.command(help='Create new migration for current branch')
@click.argument('name')
def create(name):
    """
    Create new migration with fingerprint of current git branch name
    :param name: migration name
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations
    AlembicMigrations().create(name)


@migrations.command(help='Merge branches or heads')
def merge():
    """
    Start merging heads if there are more then one
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations
    AlembicMigrations().merge()


@migrations.command(help='Show last created migration from files')
def last_revision():
    """
    Show last created migration from files. This may be not yet applied
    migration
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations
    print(AlembicMigrations().__get_last_revision__())


# @migrations.command()
# def revision_ver():
#     from faq_migrations.source.alembic_wrapper import AlembicMigrations
#     AlembicMigrations().get_revision()


@migrations.command(help='Upgrade to head')
def migrate():
    """
    Run migrations to available HEAD
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations

    am = AlembicMigrations()

    if am.migrate() is False:
        print('\nYou must merge branches first\n')
        am.merge()
        am.migrate()


@migrations.command(help='Show last migration, limit=20, upper=True')
@click.argument('limit', default=20)
@click.argument('upper', default=True)
@click.argument('verbose', default=False)
def history(limit=20, upper=True, verbose=False):
    """
    Show migration history
    :param limit: limit of output migrations
    :param upper: if True will be show new migrations (like DESC by datetime)
    :param verbose: show log entry of migration
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations

    am = AlembicMigrations()
    revisions = am.history(limit, upper)

    for revision in revisions:

        if verbose:
            script = am.get_revision(revision.revision)
            print('{}({}): {}'.format(
                revision, am.branch_name(revision), script.log_entry
            ))
            continue

        print('{} ({})'.format(
            revision, am.branch_name(revision))
        )


@migrations.command(help="Show not yet applied migrations")
def upgrade_migrations():
    """
    Show not yet applied migrations
    """
    from faq_migrations.source.alembic_wrapper import AlembicMigrations
    print(AlembicMigrations().upgrade_revisions(AlembicMigrations().current()))


@migrations.command(help="Compare local and remote history")
def compare_history():
    """
    Compare local migration sequence based of migration files and remove in
    alembic_version_history. If sequences are not same should raise Exception
    """
    from faq_migrations.source.alembic_wrapper import CompareLocalRemote

    lr = CompareLocalRemote()
    lr.compare_history()
