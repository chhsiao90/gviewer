import unittest


TEST_MODULES = [
    "gviewer.tests.test_basic",
    "gviewer.tests.test_element",
    "gviewer.tests.test_config",
    "gviewer.tests.test_error",
    "gviewer.tests.test_summary",
    "gviewer.tests.test_view",
    "gviewer.tests.test_parent",
    "gviewer.tests.test_store"
]


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    unittest.TextTestRunner().run(suite)
