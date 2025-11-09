"""initial schema

Revision ID: 20231101_0001
Revises: 
Create Date: 2023-11-01 00:00:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20231101_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    equipment_status = sa.Enum(
        "WORKING",
        "UNDER_REPAIR",
        "EXPIRED",
        "DECOMMISSIONED",
        name="equipment_status",
    )
    issue_type = sa.Enum("TECHNICAL", "MECHANICAL", "ELECTRICAL", "USER_OPERATION", name="issue_type")
    issue_status = sa.Enum("OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED", name="issue_status")
    user_role = sa.Enum("ADMIN", "TECHNICIAN", "VIEWER", name="user_role")

    equipment_status.create(op.get_bind(), checkfirst=True)
    issue_type.create(op.get_bind(), checkfirst=True)
    issue_status.create(op.get_bind(), checkfirst=True)
    user_role.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "department",
        sa.Column("department_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("department_name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "vendor",
        sa.Column("vendor_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("vendor_name", sa.String(length=200), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "user_account",
        sa.Column("user_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=50), nullable=False, unique=True),
        sa.Column("email", sa.String(length=100), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=True),
        sa.Column("role", user_role, nullable=False, server_default="VIEWER"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "refresh_token",
        sa.Column("token_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user_account.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "equipment",
        sa.Column("equipment_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("equipment_name", sa.String(length=200), nullable=False),
        sa.Column("serial_number", sa.String(length=100), nullable=True, unique=True),
        sa.Column("model_no", sa.String(length=100), nullable=True),
        sa.Column("manufacturer", sa.String(length=200), nullable=True),
        sa.Column(
            "department_id",
            sa.Integer(),
            sa.ForeignKey("department.department_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("purchase_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("status", equipment_status, nullable=False, server_default="WORKING"),
        sa.Column(
            "vendor_id",
            sa.Integer(),
            sa.ForeignKey("vendor.vendor_id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("quantity >= 0", name="ck_equipment_quantity_non_negative"),
    )
    op.create_index("ix_equipment_department_id", "equipment", ["department_id"])
    op.create_index("ix_equipment_vendor_id", "equipment", ["vendor_id"])
    op.create_index("ix_equipment_status", "equipment", ["status"])
    op.create_index("ix_equipment_expiry_date", "equipment", ["expiry_date"])

    op.create_table(
        "issue_report",
        sa.Column("issue_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "equipment_id",
            sa.Integer(),
            sa.ForeignKey("equipment.equipment_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("issue_type", issue_type, nullable=False),
        sa.Column("problem_description", sa.Text(), nullable=False),
        sa.Column("media_url", sa.String(length=500), nullable=True),
        sa.Column("date_raised", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("status", issue_status, nullable=False, server_default="OPEN"),
        sa.Column("technician", sa.String(length=100), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_issue_report_equipment_id", "issue_report", ["equipment_id"])
    op.create_index("ix_issue_report_status", "issue_report", ["status"])

    op.create_table(
        "discard_equipment",
        sa.Column("discard_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "equipment_id",
            sa.Integer(),
            sa.ForeignKey("equipment.equipment_id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("media_url", sa.String(length=500), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("discard_equipment")
    op.drop_index("ix_issue_report_status", table_name="issue_report")
    op.drop_index("ix_issue_report_equipment_id", table_name="issue_report")
    op.drop_table("issue_report")
    op.drop_index("ix_equipment_expiry_date", table_name="equipment")
    op.drop_index("ix_equipment_status", table_name="equipment")
    op.drop_index("ix_equipment_vendor_id", table_name="equipment")
    op.drop_index("ix_equipment_department_id", table_name="equipment")
    op.drop_table("equipment")
    op.drop_table("refresh_token")
    op.drop_table("user_account")
    op.drop_table("vendor")
    op.drop_table("department")

    op.execute("DROP TYPE IF EXISTS equipment_status")
    op.execute("DROP TYPE IF EXISTS issue_type")
    op.execute("DROP TYPE IF EXISTS issue_status")
    op.execute("DROP TYPE IF EXISTS user_role")
