""" Defines helper methods for typed iterable classes """

from typing import Iterable, Generator, Hashable, AbstractSet, Optional, Any

from typediter import classes # to avoid circular imports we import module
from typediter.exceptions import (
    TypeRestrictionError,
    IterableExpectedError,
    InvalidTypeRestrictionError
)

# Type Checking

def check_types( *items:Any, i_type:type ):
    """ Private helper checking the type of a number of items 
    
    Parameters
    ----------
    - ***items**
        all the items given that needs to be checked
    
    - **i_type**
        the expected type for the items
        (comparaison is made using isinstance)

    Raises
    ------
    - **typedier.exceptions.TypeRestrictionError**
        if an item with an incomptible type is found
    """
    for item in items:
        if not isinstance( item, i_type ):
            raise TypeRestrictionError( 
                f"Type-restricted operation was expecting items of type {i_type.__name__}, "
                "but received an incompatible item:\n"
                f"({type(item).__name__}): {item}"
            )

def check_object_compatibility( other:Any, *, i_type:type ):
    """ Private helper checking if an object is a compatible iterable
    
    (i) typed iterable instances gets a fast pass because we know their items type

    Parameters
    ----------
    - **other**
        the object we want to check
    
    - **i_type**
        the expected type for its items
        ( comparaison is made using isinstance )

    Raises
    ------
    - **typedier.exceptions.TypeRestrictionError**
        if an item with an incomptible type is found in the object
    
    - **typediter.exceptions.IterableExpectedError**
        if the object is not iterable
    """
    
    if isinstance( other, (classes._FrozenTypedIter, classes._MutableTypedIter) ):
        if other.i_type != i_type:
            raise TypeRestrictionError(
                f"Type-restricted operation was expecting iterable with {i_type.__name__} type items, "
                "but received an incompatible typed iterable:\n"
                f"{other}"
            )
        return
    
    if not isinstance( other, Iterable ):
        raise IterableExpectedError( f"Operation expected iterable, but received ({type(other).__name__}): {other}" )
    
    check_types( *other, i_type=i_type )


def check_i_type( i_type: Any, *, cls:Optional[type] = None ):
    """ Private helper checking if i_type is a valid type restriction 
    
    Parameters
    ----------
    - **i_type**
        the checked type restriction

    - **cls** (optional)
        the class we will be applying the type restriction to,
        used to ensure that set/frozenset based classes have 
        a hashable type restriction
    
    Raises
    ------
    - **typedier.exceptions.InvalidTypeRestrictionError**
        if i_type is not an instance of type,
        or, for set/frozenset based classes, if the given 
        i_type isn't hashable
    """
    
    if not isinstance( i_type, type ):
        raise InvalidTypeRestrictionError(
            "Provided type restriction (i_type) is not an instance of type, "
            f"Received ({type(i_type).__name__}): {i_type}"
        )
    
    # for set/frozenset we want to be sure that the 
    # given i_type produces hashable instances
    if isinstance( cls, type ) and issubclass( cls, AbstractSet ):
        if not issubclass( i_type, Hashable ):
            raise InvalidTypeRestrictionError(
                "Provided type restriction (i_type) doesn't produce hashable instances, "
                "set/frozenset based classes need hashable items, "
                f"Received ({type(i_type).__name__}): {i_type}"
            )


# Handling the generator case

def contains_generators( iterables:Iterable[Iterable] ) -> bool:
    """ Private helper returning True if 'iterables' contains an instance of a generator
    
    (i) because of the fact we sometimes do multiple operations on the operation values, 
    before passing it to be handled by the built-in iterable method,
    and generators can be used only once, we need to find when they are present to convert them to tuples
    before using them.
    """
    for iterable in iterables:
        if isinstance( iterable, Generator ):
            return True
    return False


def unpack_generators( iterables:Iterable[Iterable] ) -> tuple[ Iterable, ... ]:
    """ Private helper converting the generators present in iterables to a tuple while not modifying the other iterables
    
    (i) because of the fact we sometimes do multiple operations on the operation values, 
    before passing it to be handled by the built-in iterable method,
    and generators can be used only once, we need to convert them to tuples before carrying on.
    """
    return tuple(
        tuple(iterable) if isinstance(iterable, Generator) else iterable for iterable in iterables
    )