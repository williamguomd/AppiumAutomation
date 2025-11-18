"""Custom wrapper for Appium WebDriver calls."""
from typing import Tuple, Optional, List
from appium.webdriver import Remote
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from src.utils.wait_utils import WaitUtils


class AppiumWrapper:
    """Custom wrapper for Appium WebDriver operations."""
    
    def __init__(self, driver: Remote, wait_utils: WaitUtils = None):
        """
        Initialize AppiumWrapper.
        
        Args:
            driver: Appium WebDriver instance
            wait_utils: Optional WaitUtils instance (creates one if not provided)
        """
        self.driver = driver
        self.wait_utils = wait_utils or WaitUtils(driver)
    
    # Element Finding Methods
    def find_element(
        self,
        locator: Tuple[str, str],
        wait_for_visible: bool = True,
        timeout: Optional[int] = None
    ):
        """
        Find a single element with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            wait_for_visible: Whether to wait for element to be visible
            timeout: Optional timeout override
            
        Returns:
            WebElement if found
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        if wait_for_visible:
            if not self.wait_utils.wait_for_element_visible(locator, timeout):
                raise TimeoutException(f"Element not visible: {locator}")
        else:
            if not self.wait_utils.wait_for_element_present(locator, timeout):
                raise TimeoutException(f"Element not present: {locator}")
        
        return self.driver.find_element(*locator)
    
    def find_elements(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> List:
        """
        Find multiple elements.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout to wait for at least one element
            
        Returns:
            List of WebElements
        """
        if timeout:
            self.wait_utils.wait_for_element_present(locator, timeout)
        
        return self.driver.find_elements(*locator)
    
    def find_element_by_id(self, element_id: str, wait_for_visible: bool = True):
        """Find element by ID."""
        return self.find_element((AppiumBy.ID, element_id), wait_for_visible)
    
    def find_element_by_xpath(self, xpath: str, wait_for_visible: bool = True):
        """Find element by XPath."""
        return self.find_element((AppiumBy.XPATH, xpath), wait_for_visible)
    
    def find_element_by_accessibility_id(self, accessibility_id: str, wait_for_visible: bool = True):
        """Find element by Accessibility ID."""
        return self.find_element((AppiumBy.ACCESSIBILITY_ID, accessibility_id), wait_for_visible)
    
    def find_element_by_class_name(self, class_name: str, wait_for_visible: bool = True):
        """Find element by class name."""
        return self.find_element((AppiumBy.CLASS_NAME, class_name), wait_for_visible)
    
    def find_element_by_android_uiautomator(self, uiautomator_string: str, wait_for_visible: bool = True):
        """Find element by Android UiAutomator string."""
        return self.find_element((AppiumBy.ANDROID_UIAUTOMATOR, uiautomator_string), wait_for_visible)
    
    # Element Interaction Methods
    def click(self, locator: Tuple[str, str], timeout: int = 10):
        """
        Wait for element to be clickable and then click it.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Maximum time to wait in seconds (default: 10)
        """
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()
    
    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: Optional[int] = None):
        """
        Send keys to an element.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            text: Text to send
            clear_first: Whether to clear the field first
            timeout: Optional timeout override
        """
        if not self.wait_utils.wait_for_element_visible(locator, timeout):
            raise TimeoutException(f"Element not visible: {locator}")
        
        element = self.driver.find_element(*locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            Element text
        """
        element = self.find_element(locator, timeout=timeout)
        return element.text
    
    def is_element_present(self, locator: Tuple[str, str], timeout: Optional[int] = 5) -> bool:
        """
        Check if element is present.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            True if element is present, False otherwise
        """
        return self.wait_utils.wait_for_element_present(locator, timeout)
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: Optional[int] = 5) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            True if element is visible, False otherwise
        """
        return self.wait_utils.wait_for_element_visible(locator, timeout)
    
    def is_element_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = 5) -> bool:
        """
        Check if element is clickable.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            True if element is clickable, False otherwise
        """
        return self.wait_utils.wait_for_element_clickable(locator, timeout)
    
    # Appium-specific Methods
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 1000):
        """
        Perform swipe gesture.
        
        Args:
            start_x: Start X coordinate
            start_y: Start Y coordinate
            end_x: End X coordinate
            end_y: End Y coordinate
            duration: Duration in milliseconds
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    
    def scroll_to_element(self, locator: Tuple[str, str], direction: str = "down", max_swipes: int = 5):
        """
        Scroll to find an element.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            direction: Scroll direction ("up", "down", "left", "right")
            max_swipes: Maximum number of swipes to attempt
            
        Returns:
            WebElement if found, None otherwise
        """
        for _ in range(max_swipes):
            if self.is_element_present(locator, timeout=2):
                return self.find_element(locator)
            
            size = self.driver.get_window_size()
            width = size['width']
            height = size['height']
            
            if direction == "down":
                self.swipe(width // 2, height * 3 // 4, width // 2, height // 4)
            elif direction == "up":
                self.swipe(width // 2, height // 4, width // 2, height * 3 // 4)
            elif direction == "left":
                self.swipe(width * 3 // 4, height // 2, width // 4, height // 2)
            elif direction == "right":
                self.swipe(width // 4, height // 2, width * 3 // 4, height // 2)
        
        return None
    
    def hide_keyboard(self):
        """Hide the keyboard if visible."""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass  # Keyboard might not be visible
    
    def get_current_activity(self) -> str:
        """Get current activity name (Android)."""
        return self.driver.current_activity
    
    def get_current_package(self) -> str:
        """Get current package name (Android)."""
        return self.driver.current_package
    
    def reset_app(self):
        """Reset the app (equivalent to driver.reset())."""
        self.driver.reset()
    
    def background_app(self, seconds: int):
        """
        Put app in background for specified seconds.
        
        Args:
            seconds: Number of seconds to keep app in background
        """
        self.driver.background_app(seconds)
    
    def get_device_time(self) -> str:
        """Get device time."""
        return self.driver.get_device_time()
    
    def take_screenshot(self, filepath: str) -> bool:
        """
        Take a screenshot.
        
        Args:
            filepath: Path to save screenshot
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.save_screenshot(filepath)
            return True
        except Exception:
            return False

