"""again change size of phone number

Revision ID: c9c4d962b753
Revises: 068d2b054c70
Create Date: 2016-12-05 22:15:33.063375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9c4d962b753'
down_revision = '068d2b054c70'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE venues ALTER COLUMN phone_number TYPE varchar(50);')


def downgrade():
    pass
