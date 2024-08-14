""" Defines base classes and types for typed iterables 

(i) all classes defined here are private and not meant to be instantiated

Defined Classes
---------------
- **_FrozenTypedIter**
    Private base class for immutable typed iterables, defining the common '__new__' method

- **_MutableTypedIter**
    Private base class for mutable typed iterables, defining the common '__init__' method

    
Utility Types
-------------
- **Item_T**
    Type bound to the iterable class, describing the type of the instance's items
"""
from enum import Enum
from typing import Iterable, Generator, TypeVar, Type, Self, Generic, Literal

from typediter._helpers import check_i_type, check_object_compatibility


class _DefaultValue(Enum):
    """ Enum class with unique 'EMPTY' value used to represent the absence of initial value at instance creation
    
    (i) we use this Enum value to represent "no initial value" in the new/init dunders instead of None
    to prevent None from being a valid initial value to create a typed iterable instance.
    """
    EMPTY = 'EMPTY'

_Empty_T = Literal[ _DefaultValue.EMPTY ]

# type bound to the iterable class, 
# describing the type of the instance's items
Item_T = TypeVar( 'Item_T' ) 


class _FrozenTypedIter( Generic[Item_T] ):
    """ Private parent class for all frozen typed iterables: 'tuple' or 'frozenset' based

    **- /!\ It is not meant to be instanciated. -**

    Just defines the common 'new' dunder method:
    - checking if the 'i_type' is valid
    - checking if the given items are valid and don't break 
    the given type restriction 
    
    Attributes
    ----------
    - **i_type**
        The type restriction for the iterable's items
    """
    i_type: Type[Item_T]

    def __new__( 
            cls, 
            items: Iterable | _Empty_T = _DefaultValue.EMPTY, 
            *,
            i_type: Type[Item_T], 
            _skip_type_check: bool = False 
    ) -> Self:
        """ Checks the given 'i_type' and initial 'items' before creating the instance
        
        Parameters
        ----------
        - **items** (optional) 
            The initial items given to the iterable.

        - **i_type**
            The type restriction for the iterable's items 
        
        - **_skip_type_check** (PRIVATE)
            **- /!\ SHOULD NOT BE USED, BREAKS THE TYPE SAFETY /!\ -**
            
            internal shortcut allowing to skip the checks for 
            instance generation from trusted items.
        
        Raises
        ------
        - **typedier.exceptions.TypeRestrictionError**
            if an item in the initial 'items' is not an instance of the given 'i_type'
        
        - **typediter.exceptions.IterableExpectedError**
            if 'items' is not an iterable
        
        - **typedier.exceptions.InvalidTypeRestrictionError**
            if 'i_type' is not an instance of type, 
            or, for 'frozenset' based classes, if 'i_type' is non-hashable
        
        - **other exceptions**
            Any exception that can be raised when creating an instance of 
            the built-in iterable on which the typed iterable class is based
            (tuple / frozenset)
        """

        # if i_type is invalid, it should fail first
        check_i_type( i_type, cls=cls )

        if items is _DefaultValue.EMPTY:
            instance = super().__new__(cls)
        else:
            if not _skip_type_check:
                if isinstance( items, Generator ):
                    # because generators can be only used once
                    items = tuple(items)
                check_object_compatibility( items, i_type=i_type )
            instance = super().__new__(cls, items)  # type: ignore[call-arg]
        
        instance.i_type = i_type
        return instance


class _MutableTypedIter( Generic[Item_T] ):
    """ Private parent class for all mutable typed iterables: 'list' or 'set' based

    **- /!\ It is not meant to be instanciated. -**

    Just defines the common 'init' dunder method:
    - checking if the 'i_type' is valid
    - checking if the given items are valid and and don't break 
    the given type restriction 
    
    Attributes
    ----------
    - **i_type**
        the type restriction for the iterable items
    """
    i_type: Type[Item_T]

    def __init__( 
            self, 
            items: Iterable | _Empty_T = _DefaultValue.EMPTY, 
            *, 
            i_type: Type[Item_T], 
            _skip_type_check: bool = False 
    ):
        """ Checks the given 'i_type' and initial 'items' before initialising the instance

        Parameters
        ----------
        - **items** (optional)
            the initial items given to the iterable

        - **i_type**
            The type restriction for the iterable's items 
        
        - **_skip_type_check** (PRIVATE)
            **- /!\ SHOULD NOT BE USED, BREAKS THE TYPE SAFETY /!\ -**

            internal shortcut allowing to skip the checks for 
            instance generation from trusted items.

        Raises
        ------
        - **typedier.exceptions.TypeRestrictionError**
            if an item in the initial 'items' is not an instance of the given 'i_type'
        
        - **typediter.exceptions.IterableExpectedError**
            if 'items' is not an iterable
        
        - **typedier.exceptions.InvalidTypeRestrictionError**
            if 'i_type' is not an instance of type, 
            or, for 'set' based classes, if 'i_type' is non-hashable
        
        - **other exceptions**
            Any exception that can be raised when creating an instance of 
            the built-in iterable on which the typed iterable class is based
            (list / set)
        """

        # if i_type is invalid, it should fail first
        check_i_type( i_type, cls=type(self) )
        self.i_type = i_type

        if items is _DefaultValue.EMPTY:
            super().__init__()
        else:
            if not _skip_type_check:
                if isinstance( items, Generator ):
                    # because generators can be only used once
                    items = tuple(items)
                check_object_compatibility( items, i_type=i_type )
            super().__init__( items ) # type: ignore[call-arg]

__all__ = [ "_FrozenTypedIter", "_MutableTypedIter" ]