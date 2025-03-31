"""add postgis

Revision ID: 01_add_postgis
Create Date: 2024-02-20 10:00:00.000000
"""

import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic
revision = '01_add_postgis'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')

    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [column['name'] for column in inspector.get_columns('buildings')]

    if 'location' not in columns:
        op.add_column(
            'buildings',
            sa.Column(
                'location',
                geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326),
            ),
        )

    if 'latitude' in columns and 'longitude' in columns:
        op.execute(
            'UPDATE buildings SET location = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326) WHERE location IS NULL'
        )
        op.drop_column('buildings', 'latitude')
        op.drop_column('buildings', 'longitude')


def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [column['name'] for column in inspector.get_columns('buildings')]

    if 'latitude' not in columns:
        op.add_column('buildings', sa.Column('latitude', sa.Float()))
    if 'longitude' not in columns:
        op.add_column('buildings', sa.Column('longitude', sa.Float()))

    if 'location' in columns:
        op.execute(
            'UPDATE buildings SET latitude = ST_Y(location), longitude = ST_X(location) WHERE location IS NOT NULL'
        )
        op.drop_column('buildings', 'location')
