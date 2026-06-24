from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Read DATABASE_URL from .env
import os
from pathlib import Path

env_file = Path(__file__).resolve().parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line.startswith("DATABASE_URL="):
            os.environ.setdefault("DATABASE_URL", line.split("=", 1)[1])
            break

# Import all models so SQLModel metadata is populated
from models import *  # noqa: F401,F403
from sqlmodel import SQLModel

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using synchronous engine."""
    # Override alembic.ini URL with DATABASE_URL from .env
    from config.settings import settings
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")
    connectable = engine_from_config(
        {"url": sync_url},
        prefix="",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
