"""Example test cases for login functionality using pytest and data-driven approach."""
import pytest
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage


@pytest.mark.smoke
def test_successful_login(driver, test_case):
    """Test successful login with valid credentials."""
    # Initialize login page (automatically waits for page load)
    login_page = LoginPage(driver)
    
    # Perform login using test data - returns HomePage (automatically waits for page load)
    home_page = login_page.login(test_case["username"], test_case["password"])
    
    # Verify login was successful
    assert home_page.is_logged_in(), "User is not logged in"
    
    # Verify expected message if provided
    if "expected_message" in test_case:
        welcome_message = home_page.get_welcome_message()
        assert test_case["expected_message"] in welcome_message, \
            f"Expected message '{test_case['expected_message']}' not found"


def test_login_with_invalid_credentials(driver, test_case):
    """Test login with invalid credentials."""
    # Initialize page object (automatically waits for page load)
    login_page = LoginPage(driver)
    
    # Attempt login with invalid credentials from test data
    login_page.login(test_case["username"], test_case["password"])
    
    # Verify error message is displayed
    error_message = login_page.get_error_message()
    assert error_message != "", "Error message should be displayed for invalid credentials"
    
    # Verify expected error message if provided
    if "expected_message" in test_case:
        assert test_case["expected_message"] in error_message, \
            f"Expected error message '{test_case['expected_message']}' not found"


def test_login_with_empty_fields(driver, test_case):
    """Test login with empty username and password."""
    # Initialize page object (automatically waits for page load)
    login_page = LoginPage(driver)
    
    # Attempt login with empty fields
    login_page.click_login_button()
    
    # Verify error message is displayed
    error_message = login_page.get_error_message()
    assert error_message != "", "Error message should be displayed for empty fields"
    
    # Verify expected error message if provided
    if "expected_message" in test_case:
        assert test_case["expected_message"] in error_message, \
            f"Expected error message '{test_case['expected_message']}' not found"


# Data-driven test using pytest parametrize
@pytest.mark.parametrize("test_case_name", [
    "valid_login",
    "invalid_username",
    "invalid_password",
    "empty_credentials",
    "empty_username",
    "empty_password",
])
def test_login_scenarios_parametrized(driver, test_data_loader, test_case_name):
    """Data-driven test for login scenarios using pytest parametrize."""
    # Get test case data
    test_case = test_data_loader.get_test_case_data("login_test_data", test_case_name)
    
    username = test_case.get("username", "")
    password = test_case.get("password", "")
    expected_result = test_case.get("expected_result", "success")
    expected_message = test_case.get("expected_message", "")
    
    # Initialize page objects (automatically waits for page load)
    login_page = LoginPage(driver)
    
    # Perform login
    if username or password:
        home_page = login_page.login(username, password)  # Automatically waits for home page load
    else:
        login_page.click_login_button()
        home_page = None
    
    # Verify expected result
    if expected_result == "success":
        assert home_page is not None, f"Login should return HomePage for test case: {test_case_name}"
        assert home_page.is_logged_in(), f"Login should succeed for test case: {test_case_name}"
        if expected_message:
            welcome_message = home_page.get_welcome_message()
            assert expected_message in welcome_message, \
                f"Expected message '{expected_message}' not found for test case: {test_case_name}"
    elif expected_result == "error":
        error_message = login_page.get_error_message()
        assert error_message != "", f"Error message should be displayed for test case: {test_case_name}"
        if expected_message:
            assert expected_message in error_message, \
                f"Expected error message '{expected_message}' not found for test case: {test_case_name}"


# Alternative: Load all test cases dynamically
def test_login_all_scenarios(driver, test_data_loader):
    """Run all login test scenarios from test data file."""
    test_cases = test_data_loader.get_all_test_cases("login_test_data")
    
    for test_case in test_cases:
        test_name = test_case.get("_name", "unknown")
        username = test_case.get("username", "")
        password = test_case.get("password", "")
        expected_result = test_case.get("expected_result", "success")
        expected_message = test_case.get("expected_message", "")
        
        # Initialize page objects (automatically waits for page load)
        login_page = LoginPage(driver)
        
        # Perform login
        if username or password:
            home_page = login_page.login(username, password)  # Automatically waits for home page load
        else:
            login_page.click_login_button()
            home_page = None
        
        # Verify expected result
        if expected_result == "success":
            assert home_page is not None, f"Login should return HomePage for test case: {test_name}"
            assert home_page.is_logged_in(), f"Login should succeed for test case: {test_name}"
            if expected_message:
                welcome_message = home_page.get_welcome_message()
                assert expected_message in welcome_message, \
                    f"Expected message '{expected_message}' not found for test case: {test_name}"
        elif expected_result == "error":
            error_message = login_page.get_error_message()
            assert error_message != "", f"Error message should be displayed for test case: {test_name}"
            if expected_message:
                assert expected_message in error_message, \
                    f"Expected error message '{expected_message}' not found for test case: {test_name}"

