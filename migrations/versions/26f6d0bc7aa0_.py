"""empty message

Revision ID: 26f6d0bc7aa0
Revises: 8afa31e624d2
Create Date: 2024-03-28 17:05:29.217365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26f6d0bc7aa0'
down_revision = '8afa31e624d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth0user', schema=None) as batch_op:
        batch_op.alter_column('auth_user',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth0user', schema=None) as batch_op:
        batch_op.alter_column('auth_user',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
