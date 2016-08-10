import unittest


TEST_MODULES = [
    "gviewer.tests.test_basic",
    "gviewer.tests.test_element",
    "gviewer.tests.test_config",
    "gviewer.tests.test_error"
]


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    unittest.TextTestRunner().run(suite)
