"""add relation

Revision ID: fa4c7367a9a0
Revises: 05fda92ad378
Create Date: 2026-06-15 21:03:35.514917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa4c7367a9a0'
down_revision: Union[str, Sequence[str], None] = '05fda92ad378'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION insert_company_users()
        RETURNS trigger AS $$
        BEGIN
            INSERT INTO company("userId")
            VALUES (NEW.id);

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER insert_company_users
        AFTER INSERT ON "user"
        FOR EACH ROW
        EXECUTE FUNCTION insert_company_users();
    """)


def downgrade():
    op.execute("""
        DROP TRIGGER IF EXISTS insert_company_users ON "user";
    """)

    op.execute("""
        DROP FUNCTION IF EXISTS insert_company_users();
    """)
