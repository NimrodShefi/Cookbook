"""attempting to create the categories section of the db

Revision ID: 51c385a1c7a9
Revises: 0e359a8ee14f
Create Date: 2023-03-19 17:30:13.796417

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '51c385a1c7a9'
down_revision = '0e359a8ee14f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('recipe_categories',
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], )
    )
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_column('categories')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categories', mysql.TEXT(), nullable=False))

    op.drop_table('recipe_categories')
    op.drop_table('categories')
    # ### end Alembic commands ###