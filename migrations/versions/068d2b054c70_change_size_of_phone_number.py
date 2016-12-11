"""change size of phone number

Revision ID: 068d2b054c70
Revises: 8815afc98f10
Create Date: 2016-12-05 22:10:09.717122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '068d2b054c70'
down_revision = '8815afc98f10'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE venues ALTER COLUMN phone_number TYPE varchar(20);')


def downgrade():
    pass
