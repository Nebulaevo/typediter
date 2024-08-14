""" Defines utility functions

Utility Functions
-----------------
- **is_typediter_instance**( obj )
    returns True if argument is a typed iterable instance

- **is_typediter_subclass**( cls )
    returns True if argument is a typed iterable class

- **filter_items**( items, *, i_type )
    returns a tuple of filtered items that are instances of that type

- **get_converter_func**( typed_iterable_cls, *, i_type )
    Returns a converter function taking an iterable and returning a typed iterable instance

- **get_typesafe_tuple_converter_func**( i_type )
    Returns a converter function taking an iterable and returning a type-safe built-in tuple instance

- **get_typesafe_frozenset_converter_func**( i_type )
    Returns a converter function taking an iterable and returning a type-safe built-in frozenset instance
"""

from typing import Iterable, Callable, Generator, TypeGuard, Type, TypeVar, Any, overload

from typediter.exceptions import TypeRestrictionError, IterableExpectedError
from typediter._helpers import check_i_type, check_object_compatibility
from typediter.types import TypedIterable_T
from typediter.classes.light import (
    TypedList_lt,
    TypedTuple_lt,
    TypedSet_lt,
    TypedFrozenset_lt
)
from typediter.classes.complete import (
    TypedList,
    TypedTuple,
    TypedSet,
    TypedFrozenset
)

Item_K = TypeVar( 'Item_K' )

# remark: all complete versions inherits from the light versions
TYPED_ITERABLE_BASE_CLASSES = ( TypedList_lt, TypedTuple_lt, TypedSet_lt, TypedFrozenset_lt )

def is_typediter_instance( obj: Any | TypedIterable_T ) -> TypeGuard[ TypedIterable_T ]:
    """ Returns True if the given object is a typed iterable """
    return isinstance( obj, TYPED_ITERABLE_BASE_CLASSES )

def is_typediter_subclass( cls: Any ) -> TypeGuard[ Type[TypedIterable_T] ]:
    """ Returns True if the given class is a typed iterable class """
    if isinstance( cls, type ):
        return issubclass( cls, TYPED_ITERABLE_BASE_CLASSES )
    return False


def filter_items( items:Iterable, *, i_type:Type[Item_K] ) -> tuple[ Item_K, ... ]:
    """ Returns a tuple built from the given items, containing exclusively items that are instances of the given type """
    return tuple( item for item in items if isinstance( item, i_type ) )


@overload
def get_converter_func( typed_iterable_cls:Type[TypedList], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedList[Item_K]]: ...
@overload
def get_converter_func( typed_iterable_cls:Type[TypedList_lt], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedList_lt[Item_K]]: ...
@overload
def get_converter_func( typed_iterable_cls:Type[TypedTuple], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedTuple[Item_K]]: ...
@overload
def get_converter_func( typed_iterable_cls:Type[TypedTuple_lt], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedTuple_lt[Item_K]]: ...
@overload
def get_converter_func( typed_iterable_cls:Type[TypedSet], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedSet[Item_K]]: ...
@overload
def get_converter_func( typed_iterable_cls:Type[TypedSet_lt], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedSet_lt[Item_K]]: ...
@overload
def get_converter_func( typed_iterable_cls:Type[TypedFrozenset], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedFrozenset[Item_K]]: ...
@overload
def get_converter_func( typed_iterable_cls:Type[TypedFrozenset_lt], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedFrozenset_lt[Item_K]]: ...
def get_converter_func( typed_iterable_cls:Type[TypedIterable_T], *, i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], TypedIterable_T[Item_K]]:
    """ Returns a converter function taking an iterable and returning a typed iterable instance

    Parameters
    ----------
    - **typed_iterable_cls**
        typed iterable class we want the converter function to return an instance of

    - **i_type**
        The type restriction that will be applied to the 
        generated instance

    Returned Function Raises 
    ------------------------
    - **typediter.exceptions.TypeRestrictionError**
        if the given value contains incompatible items 
    
    - **typediter.exceptions.IterableExpectedError**
        if the given value is not an iterable

    - **typedier.exceptions.InvalidTypeRestrictionError**
        if the i_type given at generation time is invalid:
            - because it's not a type
            - or, for typed iterables based on 'set' or 'frozenset', if the given 'i_type' is not hashable
    
    - **other exceptions**
        Any exception that can be raised when creating an instance of 
        the built-in iterable on which the typed iterable class is based
        (list / tuple / set / frozenset)
    """

    def converter( items: Iterable[Item_K] ) -> TypedIterable_T[Item_K]:
        """ Function taking an iterable and returning a typed iterable instance 
        
        (i) function generated by typediter utility 'get_converter_func'

        Parameters
        ----------
        - **items**
            the iterable we want to convert

        Raises
        ------
        - **typediter.exceptions.TypeRestrictionError**
            if the given value contains incompatible items 
        
        - **typediter.exceptions.IterableExpectedError**
            if the given value is not an iterable

        - **typedier.exceptions.InvalidTypeRestrictionError**
            if the i_type given at generation time is invalid:
                - because it's not a type
                - or, for typed iterables based on 'set' or 'frozenset', if the given 'i_type' is not hashable
        
        - **other exceptions**
            Any exception that can be raised when creating an instance of 
            the built-in iterable on which the typed iterable class is based
            (list / tuple / set / frozenset)
        """
        return typed_iterable_cls( items, i_type=i_type )
        
    return converter

def get_typesafe_tuple_converter_func( i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], tuple[Item_K, ...] ]:
    """ Returns a converter function taking an iterable and returning a type-safe built-in tuple instance 
    
    Parameters
    ----------
    - **i_type**
        the type restriction that will be applied to the 
        generated instance
    
    Returned Function Raises 
    ------------------------
    - **typediter.exceptions.TypeRestrictionError**
        if the given value contains incompatible items
    
    - **typediter.exceptions.IterableExpectedError**
        if the given value is not an iterable
    
    - **typedier.exceptions.InvalidTypeRestrictionError**
        if the i_type given at generation time is not an instance of type
    
    - **other exceptions**
        Any exception that can be raised when creating an instance of tuple
    """

    def converter( items: Iterable[Item_K] ) -> tuple[Item_K, ...]:
        """ Function converting an iterable to a type-safe built-in tuple instance 
        
        (i) function generated by typediter utility 'get_typesafe_tuple_converter_func'

        Parameters
        ----------
        - **items**
            the iterable we want to convert

        Raises
        ------
        - **typediter.exceptions.TypeRestrictionError**
            if the given value contains incompatible items
        
        - **typediter.exceptions.IterableExpectedError**
            if the given value is not an iterable
        
        - **typedier.exceptions.InvalidTypeRestrictionError**
            if the i_type given at generation time is not an instance of type
        
        - **other exceptions**
            Any exception that can be raised when creating an instance of tuple
        """
        if isinstance( items, Generator ):
            # because generators can be only used once
            items = tuple(items)
        try:
            check_i_type( i_type )
            check_object_compatibility( items, i_type=i_type )
        except (TypeRestrictionError, IterableExpectedError) as err:
            raise type(err)( 
                f"Converting value to type-safe built-in tuple failed with exception:\n"
                f"{err}"
            )
        return tuple( items )

    return converter

def get_typesafe_frozenset_converter_func( i_type:Type[Item_K] 
) -> Callable[ [Iterable[Item_K]], frozenset[Item_K] ]:
    """ Returns a converter function taking an iterable and returning a type-safe built-in frozenset instance 
    
    Parameters
    ----------
    - **i_type**
        the type restriction that will be applied to the 
        generated instance
    
    Returned Function Raises 
    ------------------------
    - **typediter.exceptions.TypeRestrictionError**
        if the given value contains incompatible items 
    
    - **typediter.exceptions.IterableExpectedError**
        if the given value is not an iterable

    - **typedier.exceptions.InvalidTypeRestrictionError**
        if the i_type given at generation time is not an instance of type, 
        or if the given 'i_type' is not hashable

    - **other exceptions**
        Any exception that can be raised when creating an instance of frozenset
    """

    def converter( items: Iterable[Item_K] ) -> frozenset[Item_K]:
        """ Function converting an iterable to a type-safe built-in frozenset instance 
        
        (i) function generated by typediter utility 'get_typesafe_frozenset_converter_func'

        Parameters
        ----------
        - **items**
            the iterable we want to convert

        Raises
        ------
        - **typediter.exceptions.TypeRestrictionError**
            if the given value contains incompatible items 
        
        - **typediter.exceptions.IterableExpectedError**
            if the given value is not an iterable

        - **typedier.exceptions.InvalidTypeRestrictionError**
            if the i_type given at generation time is not an instance of type, 
            or if the given 'i_type' is not hashable

        - **other exceptions**
            Any exception that can be raised when creating an instance of frozenset
        """
        if isinstance( items, Generator ):
            # because generators can be only used once
            items = tuple(items)
        try:
            check_i_type( i_type, cls=frozenset )
            check_object_compatibility( items, i_type=i_type )
        except (TypeRestrictionError, IterableExpectedError) as err:
            raise type(err)(
                f"Converting value to type-safe built-in frozenset failed with exception:\n"
                f"{err}"
            )
        return frozenset( items )

    return converter
