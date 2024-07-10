"""update migration

Revision ID: 161e98061871
Revises: b5bd1c8edf3a
Create Date: 2024-07-10 12:25:27.088829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '161e98061871'
down_revision = 'b5bd1c8edf3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('features', schema=None) as batch_op:
        batch_op.add_column(sa.Column('speed_km', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('color', sa.String(), nullable=False))
        batch_op.drop_column('car')
        batch_op.drop_column('name')

    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.drop_column('color')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('color', sa.VARCHAR(length=128), nullable=False))

    with op.batch_alter_table('features', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), nullable=False))
        batch_op.add_column(sa.Column('car', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('color')
        batch_op.drop_column('speed_km')

    # ### end Alembic commands ###
