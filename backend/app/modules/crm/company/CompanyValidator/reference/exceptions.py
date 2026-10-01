class ReferenceError(Exception):
    """Base Reference exception."""

class IndustryNotFoundError(ReferenceError):
    pass

class CompanySizeNotFoundError(ReferenceError):
    pass

class CompanyStatusNotFoundError(ReferenceError):
    pass

class CountryNotFoundError(ReferenceError):
    pass