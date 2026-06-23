from alembic import op
import sqlalchemy as sa

revision = "001_start"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False)
    )

    op.create_table(
        "bottle_styles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("bottle", sa.String(), nullable=False),
        sa.Column("cap", sa.String(), nullable=False),
        sa.Column("rope", sa.String(), nullable=False)
    )

    op.create_table(
        "workers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False)
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("worker_id", sa.Integer(), sa.ForeignKey("workers.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True)
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("bottle_style_id", sa.Integer(), sa.ForeignKey("bottle_styles.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False)
    )

def downgrade():
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("workers")
    op.drop_table("bottle_styles")
    op.drop_table("products")
