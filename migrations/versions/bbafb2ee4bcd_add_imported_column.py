"""add imported column

Revision ID: bbafb2ee4bcd
Revises: 3cb726b2c45f
Create Date: 2016-12-07 07:50:40.511131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbafb2ee4bcd'
down_revision = '3cb726b2c45f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE venues ADD COLUMN imported boolean DEFAULT FALSE;')


def downgrade():
    pass
