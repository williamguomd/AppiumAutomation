"""Wait utilities for explicit waits in Appium tests."""
from typing import Callable, Optional, Tuple
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver import Remote


class WaitUtils:
    """Utility class for explicit waits in Appium tests."""
    
    def __init__(self, driver: Remote, timeout: int = 30):
        """
        Initialize WaitUtils.
        
        Args:
            driver: Appium WebDriver instance
            timeout: Default timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_present(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to be present in DOM.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            True if element is present, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_visible(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to be visible.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            True if element is visible, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_clickable(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to be clickable.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            True if element is clickable, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_not_present(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to not be present in DOM.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            True if element is not present, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until_not(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_not_visible(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to not be visible.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Optional timeout override
            
        Returns:
            True if element is not visible, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until_not(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_text_in_element(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for specific text to be present in element.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            text: Text to wait for
            timeout: Optional timeout override
            
        Returns:
            True if text is present, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until(EC.text_to_be_present_in_element(locator, text))
            return True
        except TimeoutException:
            return False
    
    def wait_for_custom_condition(
        self,
        condition: Callable,
        timeout: Optional[int] = None,
        message: str = ""
    ) -> bool:
        """
        Wait for custom condition to be true.
        
        Args:
            condition: Callable that returns True when condition is met
            timeout: Optional timeout override
            message: Optional error message
            
        Returns:
            True if condition is met, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until(lambda _: condition())
            return True
        except TimeoutException:
            return False
    
    def wait_for_staleness(
        self,
        element,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to become stale (removed from DOM).
        
        Args:
            element: WebElement to wait for staleness
            timeout: Optional timeout override
            
        Returns:
            True if element becomes stale, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until(EC.staleness_of(element))
            return True
        except TimeoutException:
            return False

