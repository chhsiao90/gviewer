import unittest


TEST_MODULES = [
    "gviewer.tests.test_basic",
    "gviewer.tests.test_config",
    "gviewer.tests.test_error",
    "gviewer.tests.test_summary",
    "gviewer.tests.test_parent",
    "gviewer.tests.test_store",
    "gviewer.tests.view.test_widget",
    "gviewer.tests.view.test_element"
]


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    unittest.TextTestRunner().run(suite)
