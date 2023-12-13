"""initial

Revision ID: f85dc6d413ee
Revises:
Create Date: 2023-12-05 20:00:16.442613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f85dc6d413ee"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "locations",
        sa.Column("longitude", sa.Numeric(), nullable=False),
        sa.Column("latitude", sa.Numeric(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "category_items",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category_id", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "records",
        sa.Column("value", sa.Numeric(), nullable=False),
        sa.Column("nsfw", sa.Boolean(), nullable=False),
        sa.Column("category_item_id", sa.Uuid(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_item_id"],
            ["category_items.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("records")
    op.drop_table("category_items")
    op.drop_table("locations")
    op.drop_table("categories")
    # ### end Alembic commands ###
