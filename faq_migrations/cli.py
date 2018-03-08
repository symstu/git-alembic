import click

from faq_migrations.source.alembic_wrapper import AlembicMigrations, \
    CompareLocalRemote


@click.group()
def cli():
    pass


@cli.command(help='Init alembic')
def init():
    AlembicMigrations().init()


@cli.command(help='Show current heads')
def heads():

    print('------------------------------------------')

    for head in AlembicMigrations().heads:
        print(f'{head.longdoc}')
        print(f'Branch: {al.branch_name(head)}')
        print('------------------------------------------')


@cli.command(help='Show current migration revision')
def current():
    print(AlembicMigrations().current(True))


@cli.command(help='Create new migration in current branch')
@click.argument('name')
def create(name):
    AlembicMigrations().create(name)


@cli.command(help='Merge branches')
def merge():
    AlembicMigrations().merge()


@cli.command(help='Show previous migration')
def last_revision():
    print(AlembicMigrations().__get_last_revision__())


@cli.command()
def revision_ver():
    AlembicMigrations().get_revision()


@cli.command(help='Upgrade to head')
def migrate():
    if not al.migrate():
        print('\nYou must merge branches first\n')
        AlembicMigrations().merge()
        AlembicMigrations().migrate()


@cli.command(help='Show last migration, limit=10')
@click.argument('limit', default=10)
def history(limit, upper=True):

    revisions = AlembicMigrations().history(limit, upper)

    for revision in revisions:
        print(f'{revision} | {al.branch_name(revision)}')


@cli.command(help="show future migrations")
def upgrade_migrations():
    print(AlembicMigrations().upgrade_revisions(AlembicMigrations().current()))


@cli.command(help="Compare local and remote history")
def compare_history():

    lr = CompareLocalRemote()
    lr.compare_history()
