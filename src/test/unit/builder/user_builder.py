class UserBuilder:
    def __init__(self):
        self.user = {}

    def with_fullname(self, value: str):
        self.user["fullname"] = value
        return self

    def with_email(self, value: str):
        self.user["email"] = value
        return self

    def with_password(self, value: str):
        self.user["password"] = value
        return self

    def with_enabled(self, value: str):
        self.user["enabled"] = value
        return self

    def build(self) -> dict:
        return self.user
