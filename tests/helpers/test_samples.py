import unittest
from typing import Literal, Any, Type, Iterable, Generator
import itertools 

from typediter.types import TypedIterable_T
from typediter import (
    TypedList, TypedList_lt,
    TypedTuple, TypedTuple_lt,
    TypedSet, TypedSet_lt,
    TypedFrozenset ,TypedFrozenset_lt
)

from tests.helpers import msg
from tests.helpers.types import BuiltinIterableBase_T


BuiltinIterable_T = BuiltinIterableBase_T | str | Generator

ItemsType_T = Type[str | int]
ItemsMixed_T = Literal['MIXED']
ClassesPreset_T = Literal[ 'ITERABLE', 'LIST', 'TUPLE', 'SET' ]
InitValuesVariant_T = Literal[ 'BASE', 'OPERATION', 'EMPTY' ]
InitValue_T = str | tuple | None
InitValues_T = tuple[ InitValue_T, ... ]


class TestSamples:
    """ Class aimed at providing test samples for a typed iterable testcases
    
    Each public method returns a list of samples
    Remark:
    in all the test cases, base typed iterable instances have item type of 'str'
    (the instance on which we perform the test operations)


    Attributes
    ----------
    - **test_case**
        the test case the samples are generated for
        (so that we can trigger a failure if typed iterable sample init fails)

    
    Pulic Methods
    -------------
    - **non_iterables**() 
        returns a list of items that aren't iterables

    - **items**( *, str_items ) 
        returns a list of items, exclusively str, or non-str

    - **builtin_classes**( preset ) 
        return a list of built-in iterable classes

    - **typed_iterable_classes**( preset ) 
        returns a list of typed iterable classes
    
    - **builtin_iterables**( classes, items_type, init_value_variant ) 
        returns a list of instances of the given built-in iterable classes

    - **typed_iterables**( classes, items_type, init_value_variant ) 
        returns a list of instances of the given typed iterable classes
    
    - **builtin_iterables_preset**( preset, items_type, init_value_variant ) 
        return a list of built-in iterable instances
    
    - **typed_iterables_preset**( preset, items_type, init_value_variant )
        return a list of typed iterable instances
    
    - **typed_and_builtin_iterables_preset**( preset, items_type, init_value_variant ) 
        returns a sample aggregating built-in and typed iterable instance
        
    - **all_iterables_variations**( preset ) 
        returns a sample aggregating all variations 
        of built-in and typed iterable samples with varied types.
    
    - **all_int_and_mixed_iterables_variations**( preset ) 
        returns a samples aggregating all variations 
        of built-in and typed iterable instances that are
        incompatible with a typed iterable with str items
    """

    def __init__( self, test_case:unittest.TestCase ):
        self.test_case = test_case

    def _fail( self, msg: Any = None ):
        """ private method triggering a failure of the linked test case """
        self.test_case.fail( msg )

    # ---------- Helpers ----------

    @staticmethod
    def _get_init_values( 
        items_type: ItemsType_T | ItemsMixed_T, 
        variant: InitValuesVariant_T = 'OPERATION',
    ) -> InitValues_T:
        """ Private method generating the values used to initialise an iterable instance

        /!\ Warning 
        It's important that the init values returned for 
        variant 'BASE' are UNIQUE, only one for each value of 'items_type'
        to have similar base instances when
        comparing typed and built-in iterables

        Remark:
        returns a tuple of values so that we can cycle over them
        to initialise multiple different instances
        (necessary for STR-OPERATION combo)

        Parameters
        ----------
        - **items_type**
            type of the produced items
                - str: 
                    str items only
                - int: 
                    int items only
                - "MIXED":
                    mixed type items
            
        - **variant**
            allows to vary the content of the produced iterables
                - "EMPTY":
                    empty iterable
                    (handled as a special case)

                - "BASE":
                    base iterable on which the operation is performed
                    (same as 'OPERATION' except for 'str' items_type)
                
                - "OPERATION":
                    iterable used as operation value in a test
                    (same as 'BASE' except for 'str' items_type)           
        """
        # /!\ 
        # result returned for 'BASE' have to be UNIQUE
        # only one for each value of 'items_type'

        if variant == 'EMPTY':
            # (handled as a special case)
            return (None, )

        if items_type == str:
            if variant == 'BASE':
                # repeating to test sets
                return (
                    'ABCDEABC',
                )
            else: # variant == 'OPERATION'
                # overlapping with base version
                # and with each other to test sets
                return (
                    'BDF',
                    'CDG',
                    'DEH'
                )
            
        elif items_type == int:
            return (
                ( 1, 2, 3 ),
            )
        
        else: # items_type == 'MIXED'
            return (
                ( 'B', 'D', 'F', True, False, 1, 2, 3, None ),
            )

    @staticmethod
    def _get_builtin_iterables_preset_classes(
            items_type: ItemsType_T | ItemsMixed_T = str,
            preset: ClassesPreset_T = 'ITERABLE',
            init_value_variant: InitValuesVariant_T = 'OPERATION'
    ) -> list[ Type[ BuiltinIterable_T ] ]:
        """ Private method returning the built-in iterable classes corresponding to a preset

        Remark:
        str and Generator class are added only if preset is 'ITERABLE' and:
        - str: only if items_type is str
        - Generator: only if init_value_variant is not 'EMPTY'
        
        Parameters
        ----------
        - **items_type**
            type of iterable's items
                - str: 
                    str items only
                - int: 
                    int items only
                - "MIXED":
                    mixed type items

        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets

        - **init_value_variant**
            allows to vary the content of the produced iterables
                - "EMPTY":
                    empty iterable

                - "BASE":
                    base iterable on which the operation is performed
                    (same as 'OPERATION' except for 'str' items_type)
                
                - "OPERATION":
                    iterable used as operation value in a test
                    (same as 'BASE' except for 'str' items_type)   

        """
        classes: list[ Type[ BuiltinIterable_T ] ]

        if preset == 'LIST':
            classes = [ list ]

        elif preset == 'TUPLE':
            classes = [ tuple ]
        
        elif preset == 'SET':
            classes = [ set, frozenset ]
        
        else: # preset == 'ITERABLE'
            classes = [ list, tuple, set, frozenset ]

            if items_type == str:
                # for str types, we include 'str' as built-in iterable
                classes.append(str)
            
            if init_value_variant != 'EMPTY':
                # if category is 'ITERABLE'
                # and we aren't building empty iterables
                # we include a generator
                # (handled as a special case)
                classes.append(Generator)
        
        return classes

    @staticmethod
    def _get_typed_iterables_preset_classes(
            preset: ClassesPreset_T = 'ITERABLE' 
    ) -> list[ Type[TypedIterable_T] ]:
        """ Private method returning the typed iterable classes corresponding to a preset
        
        Parameters
        ----------
        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets
        """
        classes: list[ Type[TypedIterable_T] ]
    
        if preset == 'LIST':
            classes = [ TypedList_lt, TypedList ]

        elif preset == 'TUPLE':
            classes = [ TypedTuple_lt, TypedTuple ]
        
        elif preset == 'SET':
            classes = [ 
                TypedSet_lt, TypedSet, 
                TypedFrozenset_lt, TypedFrozenset 
            ]
        
        else:
            classes = [ 
                TypedList_lt, TypedList,
                TypedTuple_lt, TypedTuple,
                TypedSet_lt, TypedSet, 
                TypedFrozenset_lt, TypedFrozenset 
            ]
        
        return classes


    # -------------------------------------------------
    # -------------------- SAMPLES --------------------
    # -------------------------------------------------

    # -------------------------------------------------
    # 1. Base Samples
     
    def non_iterables( self ) -> list:
        """ Returns a list of non iterable values """
        return [ None, 0, 1, -2.5, 1.5, False, True, ]

    def items( self, *, str_items:bool ) -> list:
        """ Returns a samples of items

        Parameters
        ----------
        - **str_items**
            switching between only str items, or only non-str items
        """
        if str_items:
            return [ 'B', 'D', 'F', 'WORD' ]
        else:
            return [ True, False, None, 1, 2, 3 ]

    def builtin_classes(
            self,
            preset: ClassesPreset_T = 'ITERABLE' 
    ) -> list[ Type[BuiltinIterable_T] ]:
        """ Returns a sample of built-in iterable classes for a given preset
        
        Parameters
        ----------
        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets
        """
        return self._get_builtin_iterables_preset_classes( 
            items_type = str, 
            preset = preset, 
            init_value_variant = 'EMPTY' # to exclude 'Generator' type 
        )

    def typed_iterable_classes( 
            self,
            preset: ClassesPreset_T = 'ITERABLE' 
    ) -> list[ Type[TypedIterable_T] ]:
        """ Returns a sample of typed iterable classes for a given preset
        
        Parameters
        ----------
        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets
        """
        return self._get_typed_iterables_preset_classes( 
            preset = preset 
        )
    
    def builtin_iterables(
            self,
            classes: Iterable[ Type[BuiltinIterable_T] ],
            items_type: ItemsType_T | ItemsMixed_T,
            init_value_variant: InitValuesVariant_T = 'OPERATION'
    ) -> list[BuiltinIterable_T]:
        """ Generate a sample of built-in iterables instances
        from a class list

        Parameters
        ----------
        - **classes**
            classes we want an instance of (only built-in iterables)
        
        - **items_type**
            type of iterable's items
                - str: 
                    str items only
                - int: 
                    int items only
                - "MIXED":
                    mixed type items

        - **init_value_variant**
            allows to vary the content of the produced iterables
                - "EMPTY":
                    empty iterable

                - "BASE":
                    base iterable on which the operation is performed
                    (same as 'OPERATION' except for 'str' items_type)
                
                - "OPERATION":
                    iterable used as operation value in a test
                    (same as 'BASE' except for 'str' items_type)
        """
        samples: list[BuiltinIterable_T] = []

        # getting the values the iterables will be initialised with
        init_values: InitValues_T = self._get_init_values(
            items_type = items_type,
            variant = init_value_variant
        )

        for cls, init_value in zip( classes, itertools.cycle(init_values) ):
            if init_value is None:
                if not issubclass( cls, Generator ):
                    samples.append( cls() )
            else:
                if issubclass( cls, Generator ):
                    samples.append( (i for i in init_value) )
                else:
                    samples.append( cls( init_value ) )
        
        return samples

    def typed_iterables(
            self,
            classes: Iterable[Type[TypedIterable_T]],
            items_type: ItemsType_T,
            init_value_variant: InitValuesVariant_T = 'OPERATION'
    ) -> list[TypedIterable_T] :
        """ Generate a sample of typed iterables instances
        from a class list

        Parameters
        ----------
        - **classes**
            classes we want an instance of (only typed iterables)
        
        - **items_type**
            typed iterable's items type

        - **init_value_variant**
            allows to vary the content of the produced iterables
                - "EMPTY":
                    empty iterable

                - "BASE":
                    base iterable on which the operation is performed
                    (same as 'OPERATION' except for 'str' items_type)
                
                - "OPERATION":
                    iterable used as operation value in a test
                    (same as 'BASE' except for 'str' items_type)

        Raises
        ------
        if the initialisation of the typed iterable samples fails,
        we call "self.test_case.fail()" and log the details
        """

        samples: list[TypedIterable_T] = []
        
        # getting the values the iterables will be initialised with
        init_values: InitValues_T = self._get_init_values(
            items_type = items_type,
            variant = init_value_variant
        )

        for cls, init_value in zip( classes, itertools.cycle(init_values) ):
            try:
                if init_value is None:
                    instance = cls( i_type=items_type )
                else:
                    instance = cls( init_value, i_type=items_type )
            
            except Exception as err:
                # if initialising typed iterables fails
                # we fail the test
                self._fail( 
                    msg.valid_init_failed(
                        cls = cls,
                        i_type = items_type,
                        init_value = init_value,
                        err = err,
                        is_sample = True
                    )
                )

            samples.append( instance )

        return samples
    
    
    # -------------------------------------------------
    # 2. Samples from presets

    def builtin_iterables_preset( 
            self, 
            preset: ClassesPreset_T = 'ITERABLE',
            items_type: ItemsType_T | ItemsMixed_T = str,
            init_value_variant: InitValuesVariant_T = 'OPERATION'
    ) -> list[BuiltinIterable_T]:
        """ Generate a sample of built-in iterables instances 
        from a preset of classes

        Parameters
        ----------
        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets

        - **items_type**
            type of iterable's items
                - str: 
                    str items only
                - int: 
                    int items only
                - "MIXED":
                    mixed type items

        - **init_value_variant**
            allows to vary the content of the produced iterables
                - "EMPTY":
                    empty iterable

                - "BASE":
                    base iterable on which the operation is performed
                    (same as 'OPERATION' except for 'str' items_type)
                
                - "OPERATION":
                    iterable used as operation value in a test
                    (same as 'BASE' except for 'str' items_type)
        """
        # getting the classes to generate depending on the category and item type expected
        classes = self._get_builtin_iterables_preset_classes( items_type, preset, init_value_variant )

        return self.builtin_iterables(
            classes = classes,
            items_type = items_type,
            init_value_variant = init_value_variant
        )

    def typed_iterables_preset(
            self,
            preset: ClassesPreset_T = 'ITERABLE',
            items_type: ItemsType_T = str,
            init_value_variant: InitValuesVariant_T = 'OPERATION'
    ) -> list[TypedIterable_T]:
        """ Generate a sample of typed iterables instances 
        from a preset of classes

        Parameters
        ----------
        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets

        - **items_type**
            typed iterable's items type

        - **init_value_variant**
            allows to vary the content of the produced iterables
                - "EMPTY":
                    empty iterable

                - "BASE":
                    base iterable on which the operation is performed
                    (same as 'OPERATION' except for 'str' items_type)
                
                - "OPERATION":
                    iterable used as operation value in a test
                    (same as 'BASE' except for 'str' items_type)

        Raises
        ------
        if the initialisation of the typed iterable samples fails,
        we call "self.test_case.fail()" and log the details
        """

        # getting the classes to generate depending on the category and item type expected
        classes = self._get_typed_iterables_preset_classes(preset)
        
        return self.typed_iterables(
            classes = classes,
            items_type = items_type,
            init_value_variant = init_value_variant
        )

    def typed_and_builtin_iterables_preset(
            self,
            preset: ClassesPreset_T = 'ITERABLE',
            items_type: ItemsType_T = str,
            init_value_variant: InitValuesVariant_T = 'OPERATION'
    ) -> list[ BuiltinIterable_T | TypedIterable_T ]:
        """ Generates a sample of both built-in and typed iterables instances 
        from a preset of classes

        aggregates samples of built-in and typed iterables instances 
        from a preset of classes with the same parameters
        
        Parameters
        ----------
        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets

        - **items_type**
            typed and built-in iterables items types

        - **init_value_variant**
            allows to vary the content of the produced iterables
                - "EMPTY":
                    empty iterable

                - "BASE":
                    base iterable on which the operation is performed
                    (same as 'OPERATION' except for 'str' items_type)
                
                - "OPERATION":
                    iterable used as operation value in a test
                    (same as 'BASE' except for 'str' items_type)
        
        Raises
        ------
        if the initialisation of the typed iterable samples fails,
        we call "self.test_case.fail()" and log the details
        """
        builtins: list = self.builtin_iterables_preset( preset, items_type, init_value_variant )
        typed: list = self.typed_iterables_preset( preset, items_type, init_value_variant )

        return builtins + typed
    
    # -------------------------------------------------
    # 3. Shortcuts

    def all_iterables_variations( 
            self, 
            preset: ClassesPreset_T = 'ITERABLE'
    ) -> list[ BuiltinIterable_T | TypedIterable_T ]:
        """ Generates a sample of all variations of both built-in and typed iterables instances 
        from a preset of classes
        
        aggregates all samples variations of built-in and typed iterable instances
        with varied parameters for operations that aren't sensible to the items types

        Parameters
        ----------
        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets

        Raises
        ------
        if the initialisation of the typed iterable samples fails,
        we call "self.test_case.fail()" and log the details
        """
        str_builtins = self.builtin_iterables_preset( preset, str, 'OPERATION' )
        int_builtins = self.builtin_iterables_preset( preset, int, 'OPERATION' )
        mix_builtins = self.builtin_iterables_preset( preset, 'MIXED', 'OPERATION' )
        builtins: list = str_builtins + int_builtins + mix_builtins

        str_typed = self.typed_iterables_preset( preset, str, 'OPERATION' )
        int_typed = self.typed_iterables_preset( preset, int, 'OPERATION' )        
        typed: list = str_typed + int_typed

        return builtins + typed
    
    def all_int_and_mixed_iterables_variations(
            self, 
            preset: ClassesPreset_T = 'ITERABLE'
    ) -> list[ BuiltinIterable_T | TypedIterable_T ]:
        """ Generates a sample of all variations that are incompatible with str typed iterable,
        from a preset of classes
        
        aggregates all samples variations of built-in and typed iterables
        that aren't compatible with a str typed iterable.

        Parameters
        ----------
        - **preset**
            shortcut name defining the used classes
                - "ITERABLE":
                    all available iterables
                - "LIST":
                    only lists
                - "TUPLE":
                    only tuples
                - "SET":
                    only sets and frozensets

        Raises
        ------
        if the initialisation of the typed iterable samples fails,
        we call "self.test_case.fail()" and log the details
        """
        int_builtins = self.builtin_iterables_preset( preset, int, 'OPERATION' )
        mix_builtins = self.builtin_iterables_preset( preset, 'MIXED', 'OPERATION' )
        builtins: list = int_builtins + mix_builtins

        typed: list = self.typed_iterables_preset( preset, int, 'OPERATION' )

        return builtins + typed