from flask import current_app, g
from src.entity.user import User
from time import time
from src.entity.user import Roles
from src.util.password import encrypt
from src.repo.user import insert
from pymysql import IntegrityError
from src.errors.custom_error import CustomError


def register(user: User):
    """
    Tries to insert a new user to the database, send verification mail to him
    """

    try:
        user.ts_registration = time()
        user.ts_last_login = time()
        user.enabled = True
        user.email_verified = False
        user.roles = [Roles.ROLE_USER]
        user.password = encrypt(user.password)

        insert(user)
    except IntegrityError as e:
        raise CustomError(
            message="User already registered",
            status_code=400,
        )

    current_app.logger.debug('User with email {} registered'.format(user.email))

    # Send event to notification service for email validation


