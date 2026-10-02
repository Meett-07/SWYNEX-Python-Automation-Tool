class SanitizerError(Exception):
    """Base error for sanitizer exception"""
    pass

class MissingFileError(SanitizerError):
    """Raised when the raw csv file cannot be found"""
    pass

class InvalidDataError(SanitizerError):
    """Raised when the data is invalid"""
    pass