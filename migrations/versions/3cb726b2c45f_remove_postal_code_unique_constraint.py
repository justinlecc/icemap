"""remove postal code unique constraint

Revision ID: 3cb726b2c45f
Revises: c9c4d962b753
Create Date: 2016-12-06 18:49:52.922463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cb726b2c45f'
down_revision = 'c9c4d962b753'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE venues DROP CONSTRAINT venues_postal_code_key;')


def downgrade():
    pass
