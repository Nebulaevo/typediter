# TypedIter
**The Type-Safe Versions of Python Built-in Iterables** 

![](https://img.shields.io/badge/Python->=_3.11-royalblue)
![](https://img.shields.io/badge/License-MIT-seagreen)


This package aims to provide type-safe versions of some python built-in iterables ( `list`, `tuple`, `set`, `frozenset` ), those can be used exactly in the same way as their built-in equivalents, except that a type of item is provided at instance creation (`i_type`), and breaking that type restriction will raise a custom `TypeRestrictionError`.
(The type-checking is executed at runtime.)




## Two Flavours of Type Safety

For each built-in iterable, this package provides 2 type-safe versions.

| Built-in class | Light version       | Complete version |
| -------------- | ------------------- | ---------------- |
| `list`         | `TypedList_lt`      | `TypedList`      |
| `tuple`        | `TypedTuple_lt`     | `TypedTuple`     |
| `set`          | `TypedSet_lt`       | `TypedSet`       |
| `frozenset`    | `TypedFrozenset_lt` | `TypedFrozenset` |

**Note:** The 'complete' versions inherits from their 'light' version equivalents. 

### Light

The "light" version (*class name ending in* **_lt**) 
only ensures the type safety of the current instance.

- Mutating methods that could insert incompatible items are overridden, they perform type checks, and will fail instead of inserting an incompatible item.
- Non-Mutating methods are all handled by the built-in class the typed iterable is based on.
So for example, a `TypedList_lt` addition, is not type-checked, and will return a built-in `list`. 
The only exception being the `copy()` method, which is overridden to return a new instance of the current typed iterable class.

The aim is to provide type safety for the current instance only, 
while avoiding slowing down operations that don't directly affect it.
This makes those operations faster, and more permissive,
but their results are downgraded to built-in iterables.



### Complete

The "complete" version ensures the type safety of the current instance, and type safety of new instances generated from it.

- Mutating methods that could insert incompatible items are overridden, they perform type checks, and will fail instead of inserting an incompatible item.
- Non-Mutating methods that used to return an instance of the same class are overridden to return an instance of the current typed iterable, for example, `list` addition returns a new `list`, so `TypedList` addition returns a new `TypedList`.
So those operations will perform type checks and fail instead of inserting an incompatible item in the operation result.

The aim is to be coherent with the built-in iterables the classes are based on. 
The downside is that it makes those operations heavier and less permissive.




## Installation

```SHELL
pip install typediter
```




## Instance Creation

```PYTHON
from typediter import (
    TypedList,
    TypedSet,
)

# Creating a list that allows only int items
# -> Any iterable can be used as initialisation value
int_list = TypedList( (1, 2, 3), i_type=int )

# Creating an empty set that allows only str items
# -> Without initialisation value, we create an empty iterable
str_set = TypedSet( i_type=str )
```

- *If one of the given items isn't an instance of the expected `i_type` the initialisation will fail with `TypeRestrictionError`.*
- *If a non-iterable initial value is given, the initialisation will fail with `IterableExpectedError`.*
- *If `i_type` is not an instance of `type`, the initialisation will fail with an `InvalidTypeRestrictionError`.*
- *For `set`/`frozenset` based classes, if `i_type` is not a hashable type, the initialisation will fail with an `InvalidTypeRestrictionError`.*




## Operations

All operations and methods defined in the built-in version are supported, and can be used in the same way.



### Mutating Operations

For both 'light' and 'complete' versions, any operation directly modifying the instance, that could insert an incompatible item is type-checked.

```PYTHON
from typediter import (
    TypedList,
    TypedSet,
)

# Creating type-restricted iterables
int_list = TypedList( (1, 2, 3), i_type=int )
int_set = TypedSet( (1, 2, 3), i_type=int )

# Same operations and methods as the built-in equivalent
int_list.append( 4 )
int_list[2] = 42
print( int_list ) # -> List[int]:[1, 2, 42, 4]

int_set.add( 4 )
int_set.update({ 5, 6 })
print( int_set ) # -> Set[int]:{1, 2, 3, 4, 5, 6}
```

- *Trying to insert an incompatible item will fail with `TypeRestrictionError`.*
- *Type-checked operations expecting an iterable, but called with something else, will fail with `IterableExpectedError`.*
- *Exceptions that are usually raised for a given operation (such as `TypeError`) can still be raised by the underlying built-in class.*



### Non-mutating operations: Light *vs* Complete versions

Operations that return a new instance and don't directly affect the current instance are handled differently between the 'light' and 'complete' versions of typed iterables:

- **light versions:** all non-mutating operations are handled by the base built-in iterable (*except `copy()` which is overridden to return a new instance of the current typed iterable class*).
- **complete versions:** non-mutating operations that return a new instance of the same class are overridden to return a new instance of the current typed iterable (for example, `list` addition returns a new `list`, so `TypedList` addition returns a new `TypedList`)

```PYTHON
# Importing both 'complete' and 'light' versions of typed list
from typediter import TypedList_lt, TypedList

# Creating instances
light_str_list = TypedList_lt( ('A', 'B', 'C'), i_type=str )
complete_str_list = TypedList( ('A', 'B', 'C'), i_type=str )

# Operation handled by the light version:
# (Not type-restricted, returns a new built-in list)
light_result = light_str_list + [ 1, 2, 3 ]
type( light_result ) # -> list

# Operation handled by the complete version:
# (Type-restricted, returns a new typed iterable)
complete_result = complete_str_list + [ 'D', 'E', 'F' ]
type( complete_result ) # -> TypedList

complete_result = complete_str_list + [ 1, 2, 3 ] # -> Fails with TypeRestrictionError
```
**for both versions:**
- *Type-checked operations expecting an iterable, but called with something else, will fail with `IterableExpectedError`.*
- *Exceptions that are usually raised for a given operation (such as `TypeError`) can still be raised by the underlying built-in class.*

**for the complete version:**
- *Trying to insert an incompatible item in the resulting instance will fail with `TypeRestrictionError`.*
- *Order matters in operations using operators ( + - ^ | ...), the first object has priority to handle the operation, if the 'complete' typed iterable is not first, the operation will be handled by the other object and type safety isn't enforced, for example: `[1,2,3]+complete_str_list` will return a built-in list and will not fail.*
- *Operations are type-restricted only if the operation is about to introduce an incompatible item in the result, operations that cannot introduce an item of the wrong type in the result aren't checked at all (like `set` `difference()` method).*




## Utility Functions

All utility functions can be imported from `typediter.utils`

```PYTHON
from typediter.utils import get_converter_func
```


### `get_converter_func( typed_iterable_cls, *, i_type )`

Returns a function converting an iterable to an instance of the given typed iterable class, restricted to the specified type (`i_type`).

**Remark:** if we create a converter for something else than a typed iterable class, or with an invalid `i_type`, it will only fail when trying to convert a value, not when creating the converter.

```PYTHON
from typediter import TypedList
from typediter.utils import get_converter_func

# Getting a function converting an iterable to a TypedList[str]
to_str_list = get_converter_func( TypedList, i_type=str )

# Converting an iterable to a typed list
str_list = to_str_list( ['A', 'B', 'C'] )

type( str_list ) # -> TypedList
```

- *The converter getter function is only meant to be used with typed iterable classes.*
- *If the iterable we are trying to convert, contains items that are not instances of `i_type`, the conversion will fail with `TypeRestrictionError`.*
- *If the value being converted is not an iterable, the conversion will fail with `IterableExpectedError`.*
- *If `i_type` is not an instance of `type`, the conversion will fail with an `InvalidTypeRestrictionError`.*
- *When converting to `set`/`frozenset` based classes, if `i_type` is not a hashable type, the conversion will fail with an `InvalidTypeRestrictionError`.*



### `get_typesafe_tuple_converter_func( i_type )`

Returns a function converting an iterable to a built-in `tuple`, restricted to the specified type (`i_type`).

**Remark:** if we create a converter with an invalid `i_type`, it will only fail when trying to convert a value, not when creating the converter.

```PYTHON
from typediter.utils import get_typesafe_tuple_converter_func

# Getting the converter functions
to_str_builtin_tuple = get_typesafe_tuple_converter_func( str )

# Converting iterables to type-safe tuple
str_builtin_tuple = to_str_builtin_tuple( ['A', 'B', 'C'] )

type( str_builtin_tuple ) # -> tuple
```

- *If the iterable we are trying to convert, contains items that are not instances of `i_type`, the conversion will fail with `TypeRestrictionError`.*
- *If the value being converted is not an iterable, the conversion will fail with `IterableExpectedError`.*
- *If `i_type` is not an instance of `type`, the conversion will fail with an `InvalidTypeRestrictionError`.*



### `get_typesafe_frozenset_converter_func( i_type )`

Returns a function converting an iterable to a built-in `frozenset`, restricted to the specified type (`i_type`).

**Remark:** if we create a converter with an invalid `i_type`, it will only fail when trying to convert a value, not when creating the converter.

```PYTHON
from typediter.utils import get_typesafe_frozenset_converter_func

# Getting the converter functions
to_str_builtin_frozenset = get_typesafe_frozenset_converter_func( str )

# Converting iterables to type-safe frozenset
str_builtin_frozenset = to_str_builtin_frozenset( ['A', 'B', 'C'] )

type( str_builtin_frozenset ) # -> frozenset
```

- *If the iterable we are trying to convert, contains items that are not instances of `i_type`, the conversion will fail with `TypeRestrictionError`.*
- *If the value being converted is not an iterable, the conversion will fail with `IterableExpectedError`.*
- *If `i_type` is not an instance of `type` or if it's not a hashable type, the conversion will fail with an `InvalidTypeRestrictionError`.*



### `filter_items( items, *, i_type )`

Function taking an iterable and a type, and returning a tuple containing only the items that are instances of that type.

```PYTHON
from typediter.utils import filter_items

filtered_items = filter_items( [1, 'A', 2, 'B'], i_type=int )

print( filtered_items ) # -> ( 1, 2 )
```



### `is_typediter_instance( obj )`

Function returning True if the given argument is an instance of a typed iterable

```PYTHON
from typediter import TypedList, TypedTuple
from typediter.utils import is_typediter_instance

# Creating typed iterable instances
str_list = TypedList( ('A', 'B', 'C'), i_type=str )
str_tuple = TypedTuple( ('A', 'B', 'C'), i_type=str )

is_typediter_instance( str_list ) # -> True
is_typediter_instance( str_tuple ) # -> True

is_typediter_instance( TypedList ) # -> False
is_typediter_instance( ['A', 'B', 'C'] ) # -> False
```



### `is_typediter_subclass( cls )`

Function returning True if the given argument is a typed iterable class

```PYTHON
from typediter import TypedList, TypedTuple
from typediter.utils import is_typediter_subclass

is_typediter_subclass( TypedList ) # -> True
is_typediter_subclass( TypedTuple ) # -> True

is_typediter_subclass( list ) # -> False
```




## Custom Exceptions

All exceptions can be imported from `typediter.exceptions`.

```PYTHON
from typediter.exceptions import TypeRestrictionError
```



### `TypeRestrictionError`
Inherits from `Exception`

Exception raised to prevent operations from breaking type restriction.



### `OperationError` 
Inherits from `Exception`

Base exception for errors related to mishandled type-checked operations.



### `InvalidTypeRestrictionError` 
Inherits from `OperationError`

Exception raised if the type restriction (`i_type`) is invalid.

Either because it's not a type, 
or because the type restriction is applied to a `set`/`frozenset` based class
and the provided `i_type` is not hashable.



### `IterableExpectedError` 
Inherits from `OperationError`

Exception raised when a type-checked operation expecting an iterable instance receives something else.




## Type hinting utils

Some utility types are made available for type hinting and can be imported from `typediter.types`

```PYTHON
from typediter.types import TypedIterable_T

foo: TypedIterable_T = ...
bar: TypedIterable_T[str] = ...
```

### `TypedIterable_T`

Any instance of a typed iterable class:
- `TypedList_lt` / `TypedList`
- `TypedTuple_lt` / `TypedTuple`
- `TypedSet_lt` / `TypedSet`
- `TypedFrozenset_lt` / `TypedFrozenset`



### `MutableTypedIterable_T`

An instance of a mutable typed iterable class:
- `TypedList_lt` / `TypedList`
- `TypedSet_lt` / `TypedSet`



### `FrozenTypedIterable_T`

An instance of an immutable typed iterable class:
- `TypedTuple_lt` / `TypedTuple`
- `TypedFrozenset_lt` / `TypedFrozenset`



## Tests

This package was tested with python **3.11.2**, **3.11.9** and **3.12.5**, on Debian 12.

It won't work with any version below **3.11**.

### Running Tests

- Download the repo
- `cd` to the root package directory
- run following command

```SHELL
python -m unittest tests
```