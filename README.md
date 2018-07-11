# FAQ Alembic Git Migration

> This module created as wrapper for Alembic and the main idea is 
> attaching real git branch, monitoring heads and auto-recommendations 
> for merging when developer creates new migration.

# How to install
```bash
pip install git+https://github.com/symstu/git-alembic.git
```

# Add CLI to your project
> As standalone manager

```python
from faq_migrations.cli import migrations


if __name__ == '__main__':
    migrations()
```

> As sub-group of click
```python
import click
from faq_migrations.cli import migrations


cli = click.Group()
cli.add_command(migrations)


if __name__ == '__main__':
    cli()
```

> and run cli

```bash
python your_manager.py migrations --help
```

# List of commands:
```
Usage: manager.py migrations [OPTIONS] COMMAND [ARGS]...

Creating of new migrations and upgrading database

Options:
  --help  Show this message and exit.

Commands:
  compare_history     Compare local and remote history
  create              Create new migration for current branch
  current             Show current migration revision
  heads               Show current heads
  history             Show last migration, limit=20, upper=True
  init                Initialize new alembic directory
  last_revision       Show previous migration
  merge               Merge branches or heads
  migrate             Upgrade to head
  upgrade_migrations  Show not yet applied migrations
```

# Config settings
```python
from faq_migrations.settings import config


# Path to your directory with alembic.ini
config.config_file_path = 'faq_migrations/migrations/' 

# Path to templates directory with alembic.ini and mako files
config.template_path = 'faq_migrations/templates/'

# Default template name
config.template_name = 'git-generic'

# Path to your directory with migrations
config.alembic_dir = 'migrations/'

# You can setup database url in this param or in alembic.ini.
# This parameter has higher priority
config.database_url = 'driver://username:pass@host:port/db_name'
```
> Before initializing new directory with migrations you must setup config 
> params.
