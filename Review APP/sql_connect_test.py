# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloud_sql_mysql_sqlalchemy_connect_connector]
import os
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy
from connect_connector import connect_with_connector

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    """Sets up connection pool for the app."""

    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    if os.environ.get("INSTANCE_CONNECTION_NAME"):
        # Either a DB_USER or a DB_IAM_USER should be defined. If both are
        # defined, DB_IAM_USER takes precedence.
        return (
            connect_with_connector()
        )

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )

def migrate_db(db: sqlalchemy.engine.base.Engine) -> None:
    """Creates the `votes` table if it doesn't exist."""
    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                "CREATE TABLE IF NOT EXISTS votes "
                "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
                "candidate VARCHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
            )
        )
        conn.commit()

db = None

# init_db lazily instantiates a database connection pool. Users of Cloud Run or
# App Engine may wish to skip this lazy instantiation and connect as soon
# as the function is loaded. This is primarily to help testing.
def init_db() -> sqlalchemy.engine.base.Engine:
    """Initiates connection to database and its' structure."""
    global db
    if db is None:
        db = connect_with_connector()
        migrate_db(db)

init_db()

with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                '''CREATE TABLE IF NOT EXISTS stu (
                stuid INTEGER PRIMARY KEY,
                name VARCHAR(50) not null,
                pid VARCHAR(20) not null,
                phone VARCHAR(20) not null)'''
            )
        )
        conn.commit()
