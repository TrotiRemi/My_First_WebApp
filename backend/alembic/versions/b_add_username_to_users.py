"""add username to users

Revision ID: b_add_username_to_users
Revises: a993006baf68
Create Date: 2025-10-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b_add_username_to_users'
down_revision = 'a993006baf68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add username column (nullable for existing rows), with length 100
    op.add_column('users', sa.Column('username', sa.String(length=100), nullable=True))
    # Create unique index on username
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Optionally, if you want to populate username from email local-part for existing users,
    # you could run an UPDATE here. We'll leave it to manual migration steps to set real usernames.


def downgrade() -> None:
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_column('users', 'username')
