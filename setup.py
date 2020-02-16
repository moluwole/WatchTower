from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='WatchTower',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description=readme(),
    install_requires=[
        'click',
        'sqlalchemy',
        'flask',
        'colorama',
        'simplejson',
        'python-dotenv',
        'nose',
        'hooks4git',
        'pytest',
        'alembic',
        'redisearch',
        'psycopg2',
        'psutil',
        'argparse',
        'requests[security]',
        'gunicorn'
    ],
    entry_points='''
        [console_scripts]
        watchshell=core.cli:main
    ''',
)
