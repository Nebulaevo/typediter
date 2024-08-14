""" Defines custom exceptions for the typediter package

Custom Exceptions
-----------------
- **_TypedIterError**
    Private base class for all typediter custom exceptions

- **TypeRestrictionError**
    Exception raised to prevent operation from breaking type restriction

- **OperationError**
    Base exception for errors related to mishandled type-checked operations

- **InvalidTypeRestrictionError**
    OperationError: the provided 'i_type' is invalid

- **IterableExpectedError**
    OperationError: A type-checked operation expected an iterable but received something else
"""

class _TypedIterError( Exception ):
    """ Private base class for all typediter custom exceptions """


class TypeRestrictionError( _TypedIterError ):
    """ Exception raised to prevent operation from breaking type restriction """


class OperationError( _TypedIterError ):
    """ Base exception for errors related to mishandled type-checked operations. """

class InvalidTypeRestrictionError( OperationError ):
    """ OperationError: the provided 'i_type' is invalid.
    
    Either because it's not a type, 
    or because the type restriction is applied to a set/frozenset based class
    and the provided 'i_type' is not hashable.
    """

class IterableExpectedError( OperationError ):
    """ OperationError: A type-checked operation expected an iterable but received something else """
