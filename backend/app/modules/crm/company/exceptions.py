class CompanyError(Exception):
    """Base COmpany exception"""

class CompanyNotFoundError(Exception):
    """Raised when a company cannot be found"""

class CompanyAlreadyExistsError(Exception):
    """Raised when a duplicate company exists."""

class OrganizationNotFoundError(Exception):
    """Raised when Organization Does not exists."""

# Company Create exception

class InvalidEmployeeCountError(Exception):
    """Raised When Employee count is below zero"""

class InvalidAnnualRevenueError(Exception):
    """Raised When Annual Revenue is below zero"""

class InvalidFoundedYearError(Exception):
    """Raised When The founded error is invalid"""

class InvalidPhoneNumber(Exception):
    """Raised When the Phone number exceed 15 digit"""

# Sorting Exception

class InvalidSortFieldError(Exception):
    """Raised When the incorrect sorting error"""

class InvalidSortOrderError(Exception):
    """Raised when order is typed incorrectly"""

class InvalidSearchError(Exception):
    """Raised when the search charchters exceed 100"""
