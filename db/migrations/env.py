import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Это конфиг Alembic, читает alembic.ini
config = context.config

# Логирование Alembic (формат из alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Пока без ORM: автоген отключён, целевая метадата отсутствует
target_metadata = None

def get_url():
    # Политика секрета: сначала переменная окружения, затем fallback на ini.
    env_url = os.getenv("AIOFFICE_DB_URL")
    if env_url:
        return env_url
    return config.get_main_option("sqlalchemy.url")

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
