"""migration

Revision ID: b5bd1c8edf3a
Revises: 9dd593c1556e
Create Date: 2024-07-09 15:43:07.371164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5bd1c8edf3a'
down_revision = '9dd593c1556e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('features', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feature_id', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    with op.batch_alter_table('rentals', schema=None) as batch_op:
        batch_op.drop_constraint('fk_rentals_vehicle_id_vehicles', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_rentals_vehicle_id_vehicles'), 'vehicles', ['vehicle_id'], ['vehicle_id'])

    with op.batch_alter_table('vehicle_features', schema=None) as batch_op:
        batch_op.drop_constraint('fk_vehicle_features_vehicle_id_vehicles', type_='foreignkey')
        batch_op.drop_constraint('fk_vehicle_features_feature_id_features', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_vehicle_features_vehicle_id_vehicles'), 'vehicles', ['vehicle_id'], ['vehicle_id'])
        batch_op.create_foreign_key(batch_op.f('fk_vehicle_features_feature_id_features'), 'features', ['feature_id'], ['feature_id'])

    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vehicle_id', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('vehicle_id')

    with op.batch_alter_table('vehicle_features', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_vehicle_features_feature_id_features'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_vehicle_features_vehicle_id_vehicles'), type_='foreignkey')
        batch_op.create_foreign_key('fk_vehicle_features_feature_id_features', 'features', ['feature_id'], ['id'])
        batch_op.create_foreign_key('fk_vehicle_features_vehicle_id_vehicles', 'vehicles', ['vehicle_id'], ['id'])

    with op.batch_alter_table('rentals', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_rentals_vehicle_id_vehicles'), type_='foreignkey')
        batch_op.create_foreign_key('fk_rentals_vehicle_id_vehicles', 'vehicles', ['vehicle_id'], ['id'])

    with op.batch_alter_table('features', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('feature_id')

    # ### end Alembic commands ###
