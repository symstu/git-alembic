import unittest
from .utils import AlembicSession


class MigratingTestCase(unittest.TestCase):

    def setUp(self):

        # Initializing git/alembic branches
        self.master = AlembicSession('master')
        self.develop = AlembicSession('develop')

    def test_branching(self):

        print('Switch to master branch')
        self.master.set_active_branch()

        print('Init alembic')
        self.master.alembic.init()

        for m in range(1, 4):
            print(f'Create migration master:{m}')
            self.master.alembic.create(f'master_{m}')

        print('Commit master and new alembic folder')
        self.master.commit('master')

        print('Migrate master database')
        self.master.alembic.migrate()

        print('Switching to develop branch')
        self.develop.set_active_branch()

        for m in range(4, 7):
            print(f'Create migration develop:{m}')
            self.develop.alembic.create(f'develop_{m}')

        print('Commit develop branch')
        self.develop.commit('develop')

        print('Migrate develop database')
        self.develop.alembic.migrate()

        print('Switch to master branch')
        self.master.set_active_branch()

        print(f'Create migration master:7')
        self.master.alembic.create(f'master_7')

        print('Commit master branch')
        self.master.commit('master')

        print('Migrate master database')
        self.master.alembic.migrate()

        print('Merge db master -> develop')
        self.master.merge(self.master.branch, self.develop.branch)

        print('Migrate master')
        self.master.alembic.migrate()

    def tearDown(self):

        self.develop.delete()
        self.master.drop_db()
        self.master.reset_to_initial()
