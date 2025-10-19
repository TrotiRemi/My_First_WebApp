from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# ✅ Ajoute le chemin du dossier backend pour que "app" soit importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.base import Base  # <-- ton Base SQLAlchemy
from app.core.config import settings  # <-- ton fichier de config (avec DATABASE_URL)

# --- Alembic configuration ---
config = context.config

# Met à jour dynamiquement l’URL de la base de données depuis ton .env
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

# Configure les logs Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata utilisée pour les migrations automatiques
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Exécute les migrations en mode 'offline'."""
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
    """Exécute les migrations en mode 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
