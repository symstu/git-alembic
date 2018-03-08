import unittest
from .utils import AlembicSession


class MigratingTestCase(unittest.TestCase):

    def setUp(self):

        # Initializing git/alembic branches
        self.master = AlembicSession('master')
        self.premaster = AlembicSession('premaster')
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
        self.master.commit('hello')

    def tearDown(self):
        pass
