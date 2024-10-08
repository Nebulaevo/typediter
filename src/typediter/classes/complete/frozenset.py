from typing import Iterable, AbstractSet, Generator

from typediter.classes import Item_T
from typediter.classes.light import TypedFrozenset_lt
from typediter._helpers import (
    check_object_compatibility,
    contains_generators,
    unpack_generators
)

class TypedFrozenset( TypedFrozenset_lt[Item_T] ):
    """ Class based on frozenset, insuring the type safety of its items, and the type safety on operations returning a new frozenset

    It can be used exactly like the built-in frozenset but its items, and some operations, are type-restricted,
    if the type restriction is broken, it fails with a TypeRestrictionError

    Inherits from frozenset, but overriding methods:
        - That could insert an incompatible item (overridden in parent 'light' version class)
        - That used to return a frozenset, to make it return a TypedFrozenset
        (for example, frozenset union returns a new frozenset instance, so TypedFrozenset union
        returns a new TypedFrozenset instance)

    Attributes
    ----------
    - **i_type**
        The type restriction for the items.
        
    Raises
    ------
    - **typediter.exceptions.TypeRestrictionError**
        Raised by a typed-checked operation to prevent
        it from inserting incompatible items in a type-safe iterable.
        (Can be raised at instance creation
        or by every operation performing type checks)
    
    - **typediter.exceptions.InvalidTypeRestrictionError**
        Raised at instance creation if the provided 'i_type':
            - is not a type
            - or is not a hashable type.
    
    - **typediter.exceptions.IterableExpectedError**
        Raised by a type-checked operation if it expected an iterable
        but received something else
        (Can be raised at instance creation
        or by every operation performing type checks)

    - **other exceptions**
        Any exception that can be raised by a built-in 'frozenset'
        for a given operation

    Usage Example
    -------------
    >>> # importing the class
    >>> from typediter import TypedFrozenset
    >>> 
    >>> # creating an instance
    >>> string_frozenset = TypedFrozenset( ('A', 'B', 'C'), i_type=str )
    >>>
    >>> # supports all frozenset operations
    >>> new_frozenset = string_frozenset & { 'D', 'E', 'F' }
    >>>
    >>> # new instances generated by non-mutating
    >>> # operations are also type-safe
    >>> type( new_frozenset ) # -> TypedFrozenset
    >>>
    >>> # Remark:
    >>> # if the non-mutating operation is handled by the built-in, a built-in is returned
    >>> builtin_and_result = { 'D', 'E', 'F' } & string_frozenset
    >>> type( builtin_and_result ) # -> set
    >>>
    >>> # trying to insert an incompatible item in the instance,
    >>> # or in a typed iterable instance generated by an operation,
    >>> # will raise a TypeRestrictionError
    >>> invalid_instance = TypedFrozenset( ( 1, 2, 3 ), i_type=str ) # will raise TypeRestrictionError
    >>> invalid_operation_result = string_frozenset & { 1, 2, 3 } # will raise TypeRestrictionError
    """
    __module__ = 'typediter.complete' # shorten class 'print' name

    # -------------------- Representation --------------------
    
    def __repr__( self ) -> str:
        typename = self.i_type.__name__
        default_representation = set(self)
        return f"Frozenset[{typename}]:{default_representation}"

    # -------------------- Overriding --------------------
    # (mutating methods overridden in parent 'light' verion class) 
    # -> Operations handled by current class should return current class instance
    
    def difference( self, *iterables: Iterable ) -> 'TypedFrozenset[Item_T]':
        """ (NO TYPE CHECK NEEDED) Return the difference of two or more sets as a new typed frozenset

        (i.e. all elements that are in this set but not the others)
        """
        # does not need type check:
        # every item retured are already present in self
        new_set = super().difference( *iterables )
        return TypedFrozenset( new_set, i_type=self.i_type, _skip_type_check=True )

    def intersection( self, *iterables: Iterable ) -> 'TypedFrozenset[Item_T]':
        """ (NO TYPE CHECK NEEDED) Return the intersection of two or more sets as a new typed frozenset

        (i.e. all elements that are in all sets)
        """
        # doesn't need type check
        # if it intersects it's already in self
        new_set = super().intersection( *iterables )
        return TypedFrozenset( new_set, i_type=self.i_type, _skip_type_check=True )
    
    def symmetric_difference( self, value: Iterable[Item_T], / ) -> 'TypedFrozenset[Item_T]':
        """ (TYPE-CHECKED) Return the symmetric difference of two sets as a new typed frozenset

        (i.e. all elements that are in exactly one of the sets)
        """
        if isinstance( value, Generator ):
            # because generators can be only used once
            value = tuple(value)

        check_object_compatibility( value, i_type=self.i_type )
        new_set = super().symmetric_difference( value )
        return TypedFrozenset( new_set, i_type=self.i_type, _skip_type_check=True )
    
    def union( self, *iterables: Iterable[Item_T] ) -> 'TypedFrozenset[Item_T]': #type: ignore[override]
        """ (TYPE-CHECKED) Return the union of sets as a new typed frozenset

        (i.e. all elements that are in either set)
        """
        if contains_generators(iterables):
            # because generators can be only used once
            iterables = unpack_generators( iterables )
            
        for iterable_obj in iterables:
            check_object_compatibility( iterable_obj, i_type=self.i_type )

        new_set = super().union( *iterables )
        return TypedFrozenset( new_set, i_type=self.i_type, _skip_type_check=True )
    
    def __sub__( self, value: AbstractSet, / ) -> 'TypedFrozenset[Item_T]':
        """ (NO TYPE CHECK NEEDED) Return self-value as a new typed frozenset """
        # does not need type-check
        # every item retured are already present in self
        new_set = super().__sub__( value )
        return TypedFrozenset( new_set, i_type=self.i_type, _skip_type_check=True )
    
    def __and__( self, value: AbstractSet, / ) -> 'TypedFrozenset[Item_T]':
        """ (NO TYPE CHECK NEEDED) Return self&value as a new typed frozenset """
        # does not need type check
        # if it intersects it's already in self
        new_set = super().__and__( value )
        return TypedFrozenset( new_set, i_type=self.i_type, _skip_type_check=True )
    
    def __or__( self, value: AbstractSet[Item_T], / ) -> 'TypedFrozenset[Item_T]': #type: ignore[override]
        """ (TYPE-CHECKED) Return self|value as a new typed frozenset """
        check_object_compatibility( value, i_type=self.i_type )
        new_set = super().__or__( value )
        return TypedFrozenset( new_set, i_type=self.i_type, _skip_type_check=True )
    
    def __xor__( self, value: AbstractSet[Item_T], / ) -> 'TypedFrozenset[Item_T]': #type: ignore[override]
        """ (TYPE-CHECKED) Return self^value as a new typed frozenset """
        check_object_compatibility( value, i_type=self.i_type )
        new_set = super().__xor__( value )
        return TypedFrozenset( new_set, i_type=self.i_type, _skip_type_check=True )