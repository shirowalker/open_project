class PasswordNotCorrectException(Exception):
    def __init__(self, args):
        self.args = args


class UserNotExistException(Exception):
    def __init__(self, args):
        self.args = args


