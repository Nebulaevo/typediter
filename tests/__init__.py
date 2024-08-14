""" Testing module for the typediter package

(i) To simplify tests, all tested instances of typed iterables have a 'str' item type (i_type),
except for some instance in test samples used as operation value, that are generated with an 'int' i_type.
"""

import unittest
from tests.test_cases import BaseTest

def load_tests( loader:unittest.TestLoader, standard_tests, pattern ) -> unittest.TestSuite:
    # Create a test suite
    test_suite = unittest.TestSuite()

    # Load base tests
    base_tests = loader.loadTestsFromTestCase(BaseTest)
    test_suite.addTests(base_tests)

    # Run base tests and collect results
    base_tests_result = unittest.TestResult()
    base_tests.run(base_tests_result)

    # Only if the base tests pass, add the other tests
    if base_tests_result.wasSuccessful():
        from tests.test_cases import (
            UtilityTests,
            CommonCopyTests,
            CommonListTupleTests,
            CommonSetTests,
            TypedListTests,
            TypedSetsTests
        )
        
        # Add the other test cases to the test suite
        test_suite.addTests(loader.loadTestsFromTestCase(UtilityTests))
        test_suite.addTests(loader.loadTestsFromTestCase(CommonCopyTests))
        test_suite.addTests(loader.loadTestsFromTestCase(CommonListTupleTests))
        test_suite.addTests(loader.loadTestsFromTestCase(CommonSetTests))
        test_suite.addTests(loader.loadTestsFromTestCase(TypedListTests))
        test_suite.addTests(loader.loadTestsFromTestCase(TypedSetsTests))
    
    return test_suite
