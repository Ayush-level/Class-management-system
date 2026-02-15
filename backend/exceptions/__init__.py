"""Custom exceptions for the service layer"""

class ServiceException(Exception):
    """Base exception for service layer"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class DatabaseException(ServiceException):
    """Database related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")

class ValidationException(ServiceException):
    """Data validation exceptions"""
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")

class NotFoundException(ServiceException):
    """Resource not found exceptions"""
    def __init__(self, message: str, resource_type: str = None):
        self.resource_type = resource_type
        super().__init__(message, "NOT_FOUND")

class DuplicateResourceException(ServiceException):
    """Duplicate resource exceptions"""
    def __init__(self, message: str, resource_type: str = None):
        self.resource_type = resource_type
        super().__init__(message, "DUPLICATE_RESOURCE")

class BusinessRuleException(ServiceException):
    """Business rule violation exceptions"""
    def __init__(self, message: str, rule: str = None):
        self.rule = rule
        super().__init__(message, "BUSINESS_RULE_VIOLATION")
