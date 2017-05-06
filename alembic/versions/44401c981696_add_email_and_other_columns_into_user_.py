"""add email and other columns into user table

Revision ID: 44401c981696
Revises: 2e8a8e95772e
Create Date: 2017-05-04 14:56:12.065534

"""

# revision identifiers, used by Alembic.
revision = '44401c981696'
down_revision = '2e8a8e95772e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=512), nullable=True))
    op.add_column('users', sa.Column('email_confirmed', sa.BOOLEAN(), nullable=False, server_default=sa.false()))
    op.add_column('users', sa.Column('register_time', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()))
    op.add_column('users', sa.Column('update_time', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'update_time')
    op.drop_column('users', 'register_time')
    op.drop_column('users', 'email_confirmed')
    op.drop_column('users', 'email')
    ### end Alembic commands ###