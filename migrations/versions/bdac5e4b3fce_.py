"""empty message

Revision ID: bdac5e4b3fce
Revises: 298f35d445a3
Create Date: 2016-10-31 16:25:56.447499

"""

# revision identifiers, used by Alembic.
revision = 'bdac5e4b3fce'
down_revision = '298f35d445a3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    ### end Alembic commands ###
