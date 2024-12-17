"""initial migration

Revision ID: 25d814bc83ed
Revises: 
Create Date: 2024-04-21 09:51:44.977108

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = '25d814bc83ed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check and create the enum type 'UserRole' manually
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'UserRole') THEN
                CREATE TYPE "UserRole" AS ENUM ('ANONYMOUS', 'AUTHENTICATED', 'MANAGER', 'ADMIN');
            END IF;
        END $$;
    """)

    # Create the 'users' table using the existing UserRole type
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('nickname', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('bio', sa.String(length=500), nullable=True),
        sa.Column('profile_picture_url', sa.String(length=255), nullable=True),
        sa.Column('linkedin_profile_url', sa.String(length=255), nullable=True),
        sa.Column('github_profile_url', sa.String(length=255), nullable=True),
        sa.Column('role', ENUM('ANONYMOUS', 'AUTHENTICATED', 'MANAGER', 'ADMIN', name='UserRole', create_type=False), nullable=False),
        sa.Column('is_professional', sa.Boolean(), nullable=True),
        sa.Column('professional_status_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=True),
        sa.Column('is_locked', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('verification_token', sa.String(), nullable=True),
        sa.Column('email_verified', sa.Boolean(), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_nickname'), 'users', ['nickname'], unique=True)


def downgrade() -> None:
    # Drop the 'users' table and indexes
    op.drop_index(op.f('ix_users_nickname'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    # Drop the 'UserRole' enum type
    op.execute("DROP TYPE IF EXISTS \"UserRole\"")
