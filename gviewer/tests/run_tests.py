import unittest


TEST_MODULES = [
    "gviewer.tests.test_basic",
    "gviewer.tests.test_element"
]


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    unittest.TextTestRunner().run(suite)
