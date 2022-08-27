"""add foreign key to post table

Revision ID: 64cc13e08e20
Revises: 336fe4c46624
Create Date: 2022-08-27 08:25:22.169444

"""
from xml.sax.handler import feature_external_ges
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64cc13e08e20'
down_revision = '336fe4c46624'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
