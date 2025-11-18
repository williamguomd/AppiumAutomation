"""Example Home Page Object."""
from appium.webdriver.common.appiumby import AppiumBy
from src.pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for Home screen."""
    
    # Locators
    WELCOME_MESSAGE = (AppiumBy.ID, "com.example.app:id/welcome_message")
    MENU_BUTTON = (AppiumBy.ID, "com.example.app:id/menu_button")
    LOGOUT_BUTTON = (AppiumBy.ID, "com.example.app:id/logout_button")
    
    def is_page_loaded(self) -> bool:
        """Check if home page is loaded."""
        return self.appium.is_element_visible(self.WELCOME_MESSAGE, timeout=5)
    
    def get_welcome_message(self) -> str:
        """Get welcome message text."""
        return self.appium.get_text(self.WELCOME_MESSAGE)
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in by verifying welcome message is visible."""
        return self.appium.is_element_visible(self.WELCOME_MESSAGE, timeout=5)

