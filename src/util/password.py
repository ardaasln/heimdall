import bcrypt


def encrypt(password: str):
    """
    Encrypt the user password with randomly generated salt and return it
    """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def check(password: str, hashed_password: str) -> bool:
    """
    Checks if hashed_password matches with password
    """
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))
