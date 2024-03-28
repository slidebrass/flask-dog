"""empty message

Revision ID: 8afa31e624d2
Revises: 4271993c2d0a
Create Date: 2024-03-28 16:48:55.071242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8afa31e624d2'
down_revision = '4271993c2d0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('breednotes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(), nullable=True))
        batch_op.drop_constraint('breednotes_id_fkey', type_='foreignkey')
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('breednotes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('breednotes_id_fkey', 'user', ['id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###