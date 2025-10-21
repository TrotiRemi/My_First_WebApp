"""add active_sessions table

Revision ID: c_add_active_sessions
Revises: b_add_username_to_users
Create Date: 2025-10-21 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c_add_active_sessions'
down_revision = 'b_add_username_to_users'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'active_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_active_sessions_id'), 'active_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_active_sessions_user_id'), 'active_sessions', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_active_sessions_user_id'), table_name='active_sessions')
    op.drop_index(op.f('ix_active_sessions_id'), table_name='active_sessions')
    op.drop_table('active_sessions')
