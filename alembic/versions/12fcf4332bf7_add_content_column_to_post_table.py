"""add content column to post table

Revision ID: 12fcf4332bf7
Revises: 0e7d49fe5538
Create Date: 2022-08-26 23:42:48.393241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12fcf4332bf7'
down_revision = '0e7d49fe5538'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts",'content')
    pass
