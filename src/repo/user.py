from flask import g
from src.entity.user import User
from src.repo.db import get_db, close_db


def insert(user: User):
    """
    Inserts the given user to database as a transaction
    """

    get_db()

    sql = "INSERT INTO user (fullname, email, password, enabled, roles,"
    sql = "{} email_verified, ts_last_login, ts_registration, last_login_ip, registration_ip".format(sql)
    sql = "{} ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(sql)

    args = (
        user.fullname, user.email, user.password, user.enabled, user._roles,
        user.email_verified, user.ts_last_login, user.ts_registration,
        user._last_login_ip, user._registration_ip
    )

    g.cursor.execute(sql, args)

    close_db()


def update_user(self, old_user: User, new_user: User):
    """
    Updates the user entity
    """
    self.db.connect()

    sql = "UPDATE user SET fullname = %s"
    args = (new_user.fullname,)

    if new_user.new_password is not None:
        sql += ", password = %s "
        args += (new_user.new_password,)

    if new_user.settings is not None:
        sql += ", settings = %s "
        args += (new_user._settings,)

    sql += "WHERE id = %s"
    args += (old_user.id,)

    self.db.cursor.execute(sql, args)

def update_last_login_data(self, user: User, ts_now: int):
    """
    Updates last login date and last login ip of the given user
    """
    self.db.connect()

    args = (
        ts_now, user._last_login_ip, user.id
    )

    self.db.cursor.execute("UPDATE user SET ts_last_login = %s, last_login_ip = %s WHERE id = %s", args)

def update_settings(self, user: User):
    """
    Updates last login date and last login ip of the given user
    """
    self.db.connect()

    args = (
        user._settings, user.id
    )

    self.db.cursor.execute("UPDATE user SET settings = %s WHERE id = %s", args)

def update_email_verified(self, email: str, is_email_verified: int):
    """
    Updates email verified field of a user
    """
    self.db.connect()

    args = (
        is_email_verified, email
    )

    self.db.cursor.execute("UPDATE user SET email_verified = %s WHERE email = %s", args)

    self.logger.debug("Email verified field changed for user {} to {}".format(email, is_email_verified))

def update_password(self, email: str, password: str):
    """
    Updates the password field of a user
    """
    self.db.connect()

    args = (
        password, email
    )

    self.db.cursor.execute("UPDATE user SET password = %s WHERE email = %s", args)

    self.logger.debug("Password updated for the user {}".format(email))

def update_email(self, old_email: str, new_email: str):
    """
    Updates the email field of a user
    """
    self.db.connect()

    args = (
        new_email, old_email
    )

    self.db.cursor.execute("UPDATE user SET email = %s WHERE email = %s", args)

    self.logger.debug("Email changed for the user {} to {}".format(old_email, new_email))

def find_by_id(self, id: int) -> User:
    """
    Return the user with given id
    """
    self.db.connect()
    self.db.cursor.execute("SELECT * FROM user WHERE id = %s", (id, ))
    row = self.db.cursor.fetchone()

    if row is None:
        return None

    return self._to_obj(row)

def find_by_email(self, email: str) -> User:
    """
    Returns the user given email
    """
    self.db.connect()

    self.db.cursor.execute("SELECT * FROM user WHERE email = %s", (email, ))
    row = self.db.cursor.fetchone()

    if row is None:
        return None

    return self._to_obj(row)

def find_by_account_id(self, account_id: int) -> list:
    self.db.connect()

    self.db.cursor.execute("SELECT * FROM user WHERE account_id = %s", (account_id))
    rows = self.db.cursor.fetchall()

    return rows

def _to_collection(self, rows: list) -> list:
    return [self._to_obj(row) for row in rows]

@staticmethod
def _to_obj(row: dict) -> User:
    return User(row)