"""empty message

Revision ID: 0500c6601314
Revises: 2b39117f40dd
Create Date: 2023-06-21 20:14:13.910932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0500c6601314'
down_revision = '2b39117f40dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('about_me', sa.String(length=160), nullable=True))
        batch_op.add_column(sa.Column('member_since', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('member_since')
        batch_op.drop_column('about_me')
        batch_op.drop_column('location')

    # ### end Alembic commands ###