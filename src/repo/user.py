import json
from flask import g
from src.entity.user import User
from src.repo.db import get_db, close_db
from typing import Union


def insert(user: User):
    """
    Inserts the given user to database as a transaction
    """

    get_db()

    sql = "INSERT INTO user (username, email, password, enabled, roles,"
    sql = "{} email_verified, ts_registration, last_login_ip, registration_ip".format(sql)
    sql = "{} ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(sql)

    args = (
        user.username, user.email, user.password, user.enabled, user._roles,
        user.email_verified, user.ts_registration, user._last_login_ip, user._registration_ip
    )

    g.cursor.execute(sql, args)

    close_db()


def find_by_email(email: str) -> Union[User, None]:
    """
    Returns the user given email
    """

    get_db()

    g.cursor.execute("SELECT * FROM user WHERE email = %s", [email])
    row = g.cursor.fetchone()

    close_db()

    if row is None:
        return None

    return User(row)


def find_by_id(user_id: int) -> Union[User, None]:
    """
    Returns the user given id
    """

    get_db()

    g.cursor.execute("SELECT * FROM user WHERE id = %s", [user_id])
    row = g.cursor.fetchone()

    close_db()

    if row is None:
        return None

    return User(row)


def update_last_login_data(user: User, ts_now: int):
    """
    Updates last login date and last login ip of the given user
    """

    get_db()

    args = (ts_now, user._last_login_ip, user.id)

    g.cursor.execute("UPDATE user SET ts_last_login = %s, last_login_ip = %s WHERE id = %s", args)

    close_db()


def update_email_verified(email: str, is_email_verified: int):
    """
    Updates email verified field of a user
    """

    get_db()

    args = (is_email_verified, email)

    g.cursor.execute("UPDATE user SET email_verified = %s WHERE email = %s", args)

    close_db()


def update_password(email: str, password: str):
    """
    Updates the password field of a user
    """

    get_db()

    args = (password, email)

    g.cursor.execute("UPDATE user SET password = %s WHERE email = %s", args)

    close_db()


def update_user(user: User):
    """
    Updates the password field of a user
    """

    get_db()

    args = (user.enabled, json.dumps(user.roles), user.email_verified, user.id)

    g.cursor.execute("UPDATE user SET enabled = %s, roles = %s, email_verified = %s WHERE id = %s", args)

    close_db()


def list_users(params: dict):
    """
    Fetches users wrt given parameters
    """
    args = []
    where_statements = []

    if params.get("name"):
        where_statements.append("(username LIKE %s OR email LIKE %s)")
        args.append("%" + params.get("name") + "%")
        args.append("%" + params.get("name") + "%")

    limit = params["size"]
    offset = limit * (params["page"] - 1)
    args.extend([limit, offset])

    sql_where = ""
    if where_statements:
        sql_where = "WHERE {}".format(" AND ".join(where_statements))

    sql = "SELECT SQL_CALC_FOUND_ROWS * " \
          "FROM user " \
          "{} " \
          "ORDER BY {} {} " \
          "LIMIT %s OFFSET %s".format(sql_where, params["order_by"], params["order_dir"])

    get_db()

    g.cursor.execute(sql, args)
    rows = g.cursor.fetchall()

    sql = "SELECT FOUND_ROWS() as total_row_count"
    g.cursor.execute(sql)
    total_row_count = g.cursor.fetchone()["total_row_count"]

    close_db()

    return rows, total_row_count
