class PeopleException(Exception):
    pass


class TranslatableException(PeopleException):

    def __init__(self, message):
        self.message = message


class PeopleImportError(TranslatableException):

    def __init__(self, message, rownumber=None, colname=None):
        super(PeopleImportError, self).__init__(message)
        self.rownumber = rownumber
        self.colname = colname
