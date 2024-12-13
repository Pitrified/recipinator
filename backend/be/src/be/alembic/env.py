"""Alembic env.py file for migrations."""

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from your_app_name import models
# from be.app.database import Base
from be.app import database

config = context.config

# target_metadata = models.Base.metadata
target_metadata = database.Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    engine = create_engine(config.get_main_option("sqlalchemy.url"))
    database.Base.metadata.bind = engine
    database.Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    engine = create_engine(config.get_main_option("sqlalchemy.url"))
    connection = engine.connect()
    context.configure(connection=connection, target_metadata=target_metadata)
    session = sessionmaker(bind=connection)()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=context._process_revision_directives,
        compare_type=True,
        compare_server_default=True,
        # compare_server_default=False,
        version_table_schema="public",
    )
    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        session.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
