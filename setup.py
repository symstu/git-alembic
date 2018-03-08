from setuptools import setup, find_packages
from os.path import join, dirname
import faq_migrations


setup(
    name='faq_migrations',
    author='Maksym Stukalo',
    author_email='stukalo.maksym@gmail.com',
    version=faq_migrations.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
        'console_scripts':
            ['faq_migrations = faq_migrations.manager']
    },
    install_requires=[
        'GitPython==2.1.5',
        'alembic==0.9.5',
        'click==6.7',
        'psycopg2==2.7.3.1',
        'SQLAlchemy==1.1.13',
        'SQLAlchemy-Utils==0.32.21'
    ]
)
