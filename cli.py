import click
from alembic_wrapper import AlembicMigrations

al = AlembicMigrations()


@click.group()
def cli():
    pass


@cli.command(help='Init alembic')
def init():
    al.init()


@cli.command(help='Show current heads')
def heads():

    print('------------------------------------------')

    for head in al.heads:
        print(f'{head.longdoc}')
        print(f'Branch: {al.branch_name(head)}')
        print('------------------------------------------')


@cli.command(help='Show current migration revision')
def current():
    print(al.current(True))


@cli.command(help='Create new migration in current branch')
@click.argument('name')
def create(name):
    al.create(name)


@cli.command(help='Merge branches')
def merge():
    al.merge()


@cli.command(help='Show previous migration')
def last_revision():
    print(al.__get_last_revision__())


@cli.command()
def revision_ver():
    al.get_revision()


@cli.command(help='Upgrade to head')
def migrate():
    if not al.migrate():
        print('\nYou must merge branches first\n')
        al.merge()


@cli.command(help='Show last migration, default=10')
@click.argument('limit', default=10)
def history(limit, upper=True):

    revisions = al.history(limit, upper)

    for revision in revisions:
        print(f'{revision} | {al.branch_name(revision)}')
