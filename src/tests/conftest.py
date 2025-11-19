"""Pytest configuration and fixtures."""
import os
import pytest
from appium import webdriver
from src.utils.config_loader import ConfigLoader
from src.utils.appium_wrapper import AppiumWrapper
from src.utils.wait_utils import WaitUtils
from src.utils.test_data_loader import TestDataLoader


@pytest.fixture(scope="session")
def config():
    """Load configuration for the test session."""
    platform = os.getenv('APPIUM_PLATFORM', None)
    device = os.getenv('APPIUM_DEVICE', None)
    config_loader = ConfigLoader(platform=platform, device=device)
    return {
        'capabilities': config_loader.get_all_capabilities(),
        'server_url': config_loader.get_server_url(),
        'platform': config_loader.get_platform(),
        'device': config_loader.get_device(),
    }


@pytest.fixture(scope="session")
def test_data_loader():
    """Provide test data loader for the session."""
    return TestDataLoader()


@pytest.fixture(scope="function")
def driver(config):
    """Create and configure Appium driver for each test."""
    # Try modern Appium approach with options (Appium 3.x+)
    try:
        if config['platform'].lower() == "android":
            from appium.options.android import UiAutomator2Options
            options = UiAutomator2Options()
            for key, value in config['capabilities'].items():
                options.set_capability(key, value)
            driver = webdriver.Remote(
                command_executor=config['server_url'],
                options=options
            )
        elif config['platform'].lower() == "ios":
            from appium.options.ios import XCUITestOptions
            options = XCUITestOptions()
            for key, value in config['capabilities'].items():
                options.set_capability(key, value)
            driver = webdriver.Remote(
                command_executor=config['server_url'],
                options=options
            )
        else:
            # Fallback to desired_capabilities
            driver = webdriver.Remote(
                command_executor=config['server_url'],
                desired_capabilities=config['capabilities']
            )
    except (ImportError, AttributeError):
        # Fallback to legacy approach (Appium 2.x and earlier)
        driver = webdriver.Remote(
            command_executor=config['server_url'],
            desired_capabilities=config['capabilities']
        )
    
    # Reset app before each test
    driver.reset()
    
    yield driver
    
    # Cleanup after test
    if driver:
        driver.quit()


@pytest.fixture(scope="function")
def appium_wrapper(driver):
    """Provide AppiumWrapper instance."""
    wait_utils = WaitUtils(driver)
    return AppiumWrapper(driver, wait_utils)


@pytest.fixture(scope="function")
def wait_utils(driver):
    """Provide WaitUtils instance."""
    return WaitUtils(driver)


@pytest.fixture(scope="function")
def test_case(request, test_data_loader):
    """
    Automatically load test case data based on test function name.
    
    Maps test function names to test case names:
    - test_successful_login -> valid_login
    - test_login_with_invalid_credentials -> invalid_username
    - test_login_with_empty_fields -> empty_credentials
    
    Can be overridden by using pytest.mark.test_case_name marker.
    """
    # Get test function name
    test_name = request.function.__name__
    
    # Remove 'test_' prefix and convert to test case name format
    # test_successful_login -> successful_login -> valid_login (via mapping)
    # test_login_with_invalid_credentials -> login_with_invalid_credentials -> invalid_username
    
    # Check if test has a marker specifying the test case name
    test_case_marker = request.node.get_closest_marker("test_case_name")
    if test_case_marker:
        test_case_name = test_case_marker.args[0] if test_case_marker.args else None
        test_data_file = test_case_marker.kwargs.get("data_file", "login_test_data")
    else:
        # Default mapping from test function name to test case name
        test_case_mapping = {
            "test_successful_login": "valid_login",
            "test_login_with_invalid_credentials": "invalid_username",
            "test_login_with_empty_fields": "empty_credentials",
        }
        
        test_case_name = test_case_mapping.get(test_name)
        test_data_file = "login_test_data"
    
    # If no mapping found, try to infer from test name
    if not test_case_name:
        # Convert test_successful_login -> valid_login
        # Convert test_login_with_invalid_credentials -> invalid_username
        base_name = test_name.replace("test_", "").replace("test_login_", "")
        
        # Try common patterns
        if "successful" in base_name or "valid" in base_name:
            test_case_name = "valid_login"
        elif "invalid" in base_name or "wrong" in base_name:
            test_case_name = "invalid_username"
        elif "empty" in base_name:
            test_case_name = "empty_credentials"
        else:
            # Default fallback
            test_case_name = base_name
    
    # Load test case data
    try:
        return test_data_loader.get_test_case_data(test_data_file, test_case_name)
    except KeyError:
        pytest.skip(f"Test case '{test_case_name}' not found in '{test_data_file}'")
