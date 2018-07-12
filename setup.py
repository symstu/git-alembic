from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='faq_migrations',
    author='Maksym Stukalo',
    author_email='stukalo.maksym@gmail.com',
    version='1.0.2',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['faq_migrations = faq_migrations.cli:cli']
    },
    install_requires=[
        'GitPython>=2.1.5',
        'alembic>=0.8.10',
        'click>=6.7',
        'psycopg2>=2.7.1',
        'SQLAlchemy>=1.1.9',
        'SQLAlchemy-Utils>=0.32.21'
    ],
    packages=find_packages(),
    data_files=[
        ('', ['README.md', ])
    ]
)
