"""Base Page Object Model class."""
from abc import ABC, abstractmethod
from appium.webdriver import Remote
from src.utils.appium_wrapper import AppiumWrapper
from src.utils.wait_utils import WaitUtils


class BasePage(ABC):
    """Abstract base class for all page objects."""
    
    def __init__(self, driver: Remote, wait_for_load: bool = True, timeout: int = 30):
        """
        Initialize BasePage.
        
        Args:
            driver: Appium WebDriver instance
            wait_for_load: Whether to wait for page to load automatically (default: True)
            timeout: Maximum time to wait for page load in seconds (default: 30)
        """
        self.driver = driver
        self.wait_utils = WaitUtils(driver)
        self.appium = AppiumWrapper(driver, self.wait_utils)
        
        # Automatically wait for page to load
        if wait_for_load:
            self.wait_for_page_load(timeout=timeout)
    
    @abstractmethod
    def is_page_loaded(self) -> bool:
        """
        Check if page is loaded.
        Must be implemented in child classes to provide page-specific load checks.
        
        Returns:
            True if page is loaded, False otherwise
        """
        pass
    
    def wait_for_page_load(self, timeout: int = 30) -> bool:
        """
        Wait for page to be loaded.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if page loaded, False otherwise
        """
        return self.wait_utils.wait_for_custom_condition(
            self.is_page_loaded,
            timeout=timeout,
            message="Page did not load within timeout"
        )
    
    def take_screenshot(self, filename: str) -> bool:
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Name of the screenshot file
            
        Returns:
            True if successful, False otherwise
        """
        import os
        screenshots_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "screenshots"
        )
        os.makedirs(screenshots_dir, exist_ok=True)
        filepath = os.path.join(screenshots_dir, filename)
        return self.appium.take_screenshot(filepath)

