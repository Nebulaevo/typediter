""" Declares helper functions aimed at representing a value as a string for failure messages """

from typing import Any, Optional, Generator, Hashable, Type

from typediter.classes import _FrozenTypedIter, _MutableTypedIter

# -------------------- Individual reprs --------------------

def type_name( value:type ) -> str:
    """ Returns string representation of a type
    
    Parameters
    ----------
    - **value**
        the type we want to extract the name of
    """
    return value.__name__ 

def value_with_type( 
        value: Any, 
        v_type: Optional[type] = None 
) -> str:
    """ return a string representation of a value as: "type: value"
    
    Parameters
    ----------
    - **value**
        the value we want a string representation of
    
    - **v_type** (optional)
        type to display instead of the real type of the value
    """
    
    # formatting type for logging
    if v_type is None:
        v_type = type( value )
    
    if issubclass( v_type, (_FrozenTypedIter, _MutableTypedIter) ):
        i_type = None
        if isinstance( value, (_FrozenTypedIter, _MutableTypedIter) ):
            i_type = value.i_type
        type_repr = typediter_class( v_type, i_type )
    else:
        type_repr = type_name( v_type )

    # formatting value for logging
    if value is None:
        value = '- None -'
    elif isinstance( value, (Generator, frozenset, _FrozenTypedIter, _MutableTypedIter) ):
        # Generator: otherwise it doesn't show the items
        # frozenset, _FrozenTypedIter, _MutableTypedIter: to have a cleaner log 
        # ( because default typeriter and frozenset reprs already includes class and type )
        value = tuple( value ) # type: ignore [arg-type]
    
    return f"{type_repr}: {value}"

# -------------------- Helper reprs --------------------

def i_type_validity( i_type:Any ) -> str:
    """ Returns string describing the given i_type
    - if it is a valid type
    - if this type is hashable 
    (set/frozenset based classes require hashable i_type)

    Parameters
    ----------
    - **i_type**
        the i_type used in the test
    """
    if isinstance( i_type, type ):
        is_type_instance = 'Yes'
        if issubclass( i_type, Hashable ):
            is_hashable = 'Yes'
        else:
            is_hashable = 'No'

    else:
        is_type_instance = f'No, received {value_with_type( i_type )}'
        is_hashable = '-'

    i_type_validity_repr = f"is type instance: {is_type_instance}\nis hashable type: {is_hashable}"

    return i_type_validity_repr

def typediter_class(
        cls: Type[_FrozenTypedIter | _MutableTypedIter],
        i_type: Any = None # simpler to handle invalid 'i_type' testing
) -> str:
    """ Returns string representation of a typediter class
    
    Parameters
    ----------
    - **cls**
        the typediter class we want a representation of
    
    - **i_type** (optional)
        item type restriction to add for more details
        (type is Any because in some cases it gets an invalid i_type for testing)
    """
    repr_str = type_name( cls )
    if isinstance( i_type, type ):
        type_repr = type_name( i_type )
        repr_str += f"[{type_repr}]"
    
    return repr_str

def typediter_instance( 
        inst: _FrozenTypedIter | _MutableTypedIter, 
        init_value: Optional[Any] = None 
) -> str:
    """ Returns string representation of a typediter instance

    Parameters
    ----------
    - **inst**
        the typediter instance we want a representation of
    
    - **init_value** (optional)
        initialisation value of the instance for more details
    """
    repr_str = str(inst)

    if not init_value is None:
        init_value_repr = (
            "\n[ intialisation value ]\n"
            f"{ value_with_type( init_value ) }"
        )
        repr_str += init_value_repr
    
    return repr_str

# -------------------- titled data --------------------

def titled_data( title:str, data: str | list[str] ) -> str:
    """ Returns titled data to format message

    to make the logged data more clear in the messages we add a title to it

    (i) to simplify the *args operations cases
    ( where the operation value is a list of samples instead of one sample )
    we allow data_string to be a list of strings, so that they can all be displayed under
    the same title

    Parameters
    ----------
    - **title**
        the title that will be displayed for the data
    
    - **data**
        the data representation string
        can be a string, or a list of strings
    """
    
    if isinstance( data, list ):
        # only used for '*args' type operations 
        # (only in assertions.operation_asserts)
        data_reprs = [ f"- {data_repr}" for data_repr in data ]
        data_string = '\n'.join( data_reprs )
        return titled_data( title, data_string )
    
    else: # str
        return f" \033[01m[ {title} ]\033[00m\n{data}"

# -------------------- title formatter --------------------

def red_title( text:str ) -> str:
    """ Retrurns a formatted string that will be displayed in red in the terminal """
    return f"\033[01m\033[91m❌ {text} \033[00m"