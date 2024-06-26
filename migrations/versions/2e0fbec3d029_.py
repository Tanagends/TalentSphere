"""empty message

Revision ID: 2e0fbec3d029
Revises: cbfb2fa0c4a2
Create Date: 2024-04-10 17:44:01.511437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e0fbec3d029'
down_revision = 'cbfb2fa0c4a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('academies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(length=250), nullable=True))

    with op.batch_alter_table('clubs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(length=250), nullable=True))

    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(length=250), nullable=True))

    with op.batch_alter_table('scouts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(length=250), nullable=True))

    with op.batch_alter_table('sponsors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(length=250), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sponsors', schema=None) as batch_op:
        batch_op.drop_column('bio')

    with op.batch_alter_table('scouts', schema=None) as batch_op:
        batch_op.drop_column('bio')

    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.drop_column('bio')

    with op.batch_alter_table('clubs', schema=None) as batch_op:
        batch_op.drop_column('bio')

    with op.batch_alter_table('academies', schema=None) as batch_op:
        batch_op.drop_column('bio')

    # ### end Alembic commands ###
