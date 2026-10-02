#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Add paused_until to DagModel.

Revision ID: 139db94726b3
Revises: 90e4d18ccadf
Create Date: 2026-10-02 16:20:05.000000

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

from airflow.migrations.utils import disable_sqlite_fkeys
from airflow.utils.sqlalchemy import UtcDateTime

revision = "139db94726b3"
down_revision = "90e4d18ccadf"
branch_labels = None
depends_on = None
airflow_version = "3.4.0"


def upgrade():
    """Add paused_until to DagModel."""
    with disable_sqlite_fkeys(op):
        with op.batch_alter_table("dag", schema=None) as batch_op:
            batch_op.add_column(sa.Column("paused_until", UtcDateTime, nullable=True))
            batch_op.create_index("idx_dag_paused_until", ["paused_until"], unique=False)
            batch_op.create_check_constraint(
                "dag_paused_until_valid",
                "paused_until IS NULL OR is_paused OR is_draining",
            )


def downgrade():
    """Remove paused_until from DagModel."""
    with disable_sqlite_fkeys(op):
        with op.batch_alter_table("dag", schema=None) as batch_op:
            batch_op.drop_constraint("dag_paused_until_valid", type_="check")
            batch_op.drop_index("idx_dag_paused_until")
            batch_op.drop_column("paused_until")
