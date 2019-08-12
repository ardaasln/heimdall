import json


class User:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.username = data.get("username")
        self.email = data.get("email")
        self.password = data.get("password")
        self.enabled = data.get("enabled")
        self._roles = data.get("roles")
        self.email_verified = data.get("email_verified")
        self.ts_last_login = data.get("ts_last_login")
        self.ts_registration = data.get("ts_registration")
        self._registration_ip = data.get("registration_ip")
        self._last_login_ip = data.get("last_login_ip")

    @property
    def registration_ip(self):
        if self._registration_ip is None:
            return None
        return json.loads(self._registration_ip)

    @registration_ip.setter
    def registration_ip(self, value):
        self._registration_ip = json.dumps(value)

    @property
    def last_login_ip(self):
        if self._last_login_ip is None:
            return None
        return json.loads(self._last_login_ip)

    @last_login_ip.setter
    def last_login_ip(self, value):
        self._last_login_ip = json.dumps(value)

    @property
    def roles(self):
        if self._roles is None:
            return None
        return json.loads(self._roles)

    @roles.setter
    def roles(self, value):
        self._roles = json.dumps(value)

    def jwt_payload(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "enabled": self.enabled,
            "roles": self.roles,
            "email_verified": self.email_verified,
            "ts_registration": self.ts_registration,
            "last_login_ip": self.last_login_ip
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "enabled": self.enabled,
            "roles": self.roles,
            "email_verified": self.email_verified,
            "ts_registration": self.ts_registration,
            "last_login_ip": self.last_login_ip,
        }


class Roles:
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"
