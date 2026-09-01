"""fixed student table relationship

Revision ID: 84447aa2037e
Revises: 85370c739b61
Create Date: 2026-09-01 04:30:40.700048

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '84447aa2037e'
down_revision = '85370c739b61'
branch_labels = None
depends_on = None


def upgrade():
    # Create PostgreSQL enum type first
    gender_enum = postgresql.ENUM(
        'MALE',
        'FEMALE',
        name='gender'
    )

    gender_enum.create(op.get_bind(), checkfirst=True)

    # Add gender column
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'gender',
                gender_enum,
                nullable=False
            )
        )

        batch_op.create_index(
            batch_op.f('ix_student_gender'),
            ['gender'],
            unique=False
        )


def downgrade():
    # Remove column/index first
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_student_gender'))
        batch_op.drop_column('gender')

    # Then remove PostgreSQL enum type
    gender_enum = postgresql.ENUM(
        'MALE',
        'FEMALE',
        name='gender'
    )

    gender_enum.drop(op.get_bind(), checkfirst=True)