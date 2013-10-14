class PeopleException(Exception):
    pass


class TranslatableException(PeopleException):
    def __init__(self, msg):
        self.msg = msg


class PeopleImportError(TranslatableException):
    pass
