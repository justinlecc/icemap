"""change venue name size

Revision ID: 8815afc98f10
Revises: 2439a79daa14
Create Date: 2016-12-05 20:51:48.025459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8815afc98f10'
down_revision = '2439a79daa14'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE venues ALTER COLUMN name TYPE varchar(200);')


def downgrade():
    pass
