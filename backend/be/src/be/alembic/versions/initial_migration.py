"""Initial migration

Revision ID: 0001
Revises:
Create Date: 
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "simple_recipe",
        sa.Column("RecipeID", sa.Integer(), nullable=False),
        sa.Column("Title", sa.String(), nullable=True),
        sa.Column("CaptionOriginal", sa.String(), nullable=True),
        sa.Column("CaptionClean", sa.String(), nullable=True),
        sa.Column("HasUrlMedia", sa.Integer(), nullable=True),
        sa.Column("HasVideoUrlMedia", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("RecipeID"),
    )
    op.create_table(
        "author",
        sa.Column("AuthorID", sa.Integer(), nullable=False),
        sa.Column("Name", sa.String(), nullable=True),
        sa.Column("PageLink", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("AuthorID"),
    )
    op.create_table(
        "tag",
        sa.Column("TagID", sa.Integer(), nullable=False),
        sa.Column("Name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("TagID"),
    )
    op.create_table(
        "recipe_author",
        sa.Column("RecipeID", sa.Integer(), nullable=False),
        sa.Column("AuthorID", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["AuthorID"],
            ["author.AuthorID"],
        ),
        sa.ForeignKeyConstraint(
            ["RecipeID"],
            ["simple_recipe.RecipeID"],
        ),
        sa.PrimaryKeyConstraint("RecipeID", "AuthorID"),
    )
    op.create_table(
        "recipe_tags",
        sa.Column("RecipeID", sa.Integer(), nullable=False),
        sa.Column("TagID", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["RecipeID"],
            ["simple_recipe.RecipeID"],
        ),
        sa.ForeignKeyConstraint(
            ["TagID"],
            ["tag.TagID"],
        ),
        sa.PrimaryKeyConstraint("RecipeID", "TagID"),
    )


def downgrade():
    op.drop_table("recipe_tags")
    op.drop_table("recipe_author")
    op.drop_table("tag")
    op.drop_table("author")
    op.drop_table("simple_recipe")
