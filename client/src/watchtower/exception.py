class AuthenticationError(Exception):
    def __init__(self, message, errors=None):
        self.message = (message,)
        self.errors = errors

        super().__init__(f"message: {self.message}, errors: {self.errors}")


class ValidationError(Exception):
    def __init__(self, message=None, errors=None):
        if message is None:
            self.message = "Unable to validate credentials"
        else:
            self.message = message

        self.errors = errors
        super().__init__(f"message: {self.message}, errors: {self.errors}")


class ServerNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"message: Could not access server. Check BASE URL")


class ConfigFileNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"message: .watchtower.ini file not found")


class FailedErrorLog(Exception):
    def __init__(self):
        super().__init__(
            f"message: Failed to save Log files. Check if the server is up"
        )
