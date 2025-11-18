"""Base test class for all test cases (pytest-based)."""
from abc import ABC


class BaseTest(ABC):
    """
    Abstract base test class for class-based tests.
    
    Note: With pytest, you typically don't need to inherit from a base class.
    Instead, use fixtures (driver, appium_wrapper, wait_utils, test_data_loader)
    directly in your test functions.
    
    This class is provided for those who prefer class-based tests.
    Simply use pytest fixtures as method parameters in your test methods.
    
    Example:
        class TestMyFeature(BaseTest):
            def test_something(self, driver, test_data_loader):
                # Use fixtures as method parameters
                page = MyPage(driver)
                test_data = test_data_loader.get_test_case_data("data", "case1")
                assert page.is_loaded()
    
    Available fixtures (use as method parameters):
    - driver: Appium WebDriver instance
    - appium_wrapper: AppiumWrapper instance
    - wait_utils: WaitUtils instance
    - test_data_loader: TestDataLoader instance
    - config: Configuration dictionary
    """
    pass
