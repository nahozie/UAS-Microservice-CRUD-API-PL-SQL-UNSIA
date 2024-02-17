"""Pesan migrasi

Revision ID: d2226c710541
Revises: d4e70b3630c7
Create Date: 2023-12-16 22:44:26.798035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2226c710541'
down_revision = 'd4e70b3630c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=256), nullable=False))
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.drop_column('encrypted_password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('encrypted_password', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.alter_column('username',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.drop_column('password')

    # ### end Alembic commands ###
