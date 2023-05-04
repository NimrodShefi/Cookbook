"""turning the values of name and email in Users to lowercase as they get saved for consistency

Revision ID: ae529c5ac723
Revises: 51c385a1c7a9
Create Date: 2023-05-04 12:48:18.350834

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ae529c5ac723'
down_revision = '51c385a1c7a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index('email')
        batch_op.drop_column('email')
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=200), nullable=False))
        batch_op.add_column(sa.Column('email', mysql.VARCHAR(length=200), nullable=False))
        batch_op.create_index('email', ['email'], unique=False)

    # ### end Alembic commands ###