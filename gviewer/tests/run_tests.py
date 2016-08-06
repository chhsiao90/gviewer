import unittest


TEST_MODULES = [
    "gviewer.tests.test_basic"
]


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    unittest.TextTestRunner().run(suite)
