class PeopleException(Exception):
    pass


class TranslatableException(PeopleException):

    def __repr__(self):
        return 'TranslatableException({})'.format(self.message)

    def __init__(self, message):
        self.message = message


class PeopleImportError(TranslatableException):

    def __repr__(self):
        base = 'PeopleImportError(message="{}", rownumber={}, colname="{}")'
        return base.format(self.message, self.rownumber, self.colname or '')

    def __init__(self, message, rownumber=None, colname=None):
        super(PeopleImportError, self).__init__(message)
        self.rownumber = rownumber
        self.colname = colname
