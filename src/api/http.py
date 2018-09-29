from src.errors.custom_error import CustomError
from src.util.jwt_ops import decode
from jwt import InvalidTokenError
from flask import current_app, g


class Http(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)

    @staticmethod
    def auth(token: str, roles: list = None):
        """
        Authenticates the jwt and authorizes the caller. If everything is fine returns the claims
        """
        if token is None:
            raise CustomError(
                message="Token not found",
                status_code=400
            )

        try:
            decoded = decode(token, current_app.config["JWT_SECRET"])
        except InvalidTokenError:
            raise CustomError(
                message="Token not valid",
                status_code=401
            )

        if roles is None:
            g.user = decoded
            return

        skip = False

        for role in roles:
            if role in decoded["roles"]:
                skip = True
                break
            else:
                skip = False

        if not skip:
            raise CustomError(
                message="Access forbidden",
                status_code=403,
            )

        g.user = decoded
