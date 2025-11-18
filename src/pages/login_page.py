"""Example Login Page Object."""
from appium.webdriver.common.appiumby import AppiumBy
from src.pages.base_page import BasePage
from src.pages.home_page import HomePage


class LoginPage(BasePage):
    """Page Object for Login screen."""
    
    # Locators
    USERNAME_FIELD = (AppiumBy.ID, "com.example.app:id/username")
    PASSWORD_FIELD = (AppiumBy.ID, "com.example.app:id/password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.example.app:id/login_button")
    ERROR_MESSAGE = (AppiumBy.ID, "com.example.app:id/error_message")
    
    def is_page_loaded(self) -> bool:
        """Check if login page is loaded."""
        return self.appium.is_element_visible(self.USERNAME_FIELD, timeout=5)
    
    def login(self, username: str, password: str) -> HomePage:
        """
        Perform complete login action.
        
        Args:
            username: Username to login with
            password: Password to login with
            
        Returns:
            HomePage instance after successful login
        """
        self.appium.send_keys(self.USERNAME_FIELD, username)
        self.appium.send_keys(self.PASSWORD_FIELD, password)
        self.appium.click(self.LOGIN_BUTTON)
        return HomePage(self.driver)

