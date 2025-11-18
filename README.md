# Appium Automation Framework

A scalable, maintainable Appium testing framework built with Python using Page Object Model (POM) pattern. Supports both **iOS** and **Android** platforms.

## Features

- **Multi-Platform Support**: Configurable for both iOS and Android
- **Page Object Model**: Clean separation of page logic from test logic
- **Automatic Page Load**: Page objects automatically wait for page load in constructor
- **Driver Reset**: Automatic app reset before each test using `driver.reset()`
- **JSON Configuration**: Centralized configuration for app build, version, and environment
- **Custom Appium Wrapper**: Reusable wrapper for common Appium operations
- **Wait-Utils Layer**: Explicit waits only (no implicit waits) for reliable test execution
- **UV Package Management**: Fast Python package management with `uv`
- **Pytest Framework**: Modern testing framework with fixtures, parametrization, and markers
- **Implicit Test Data Loading**: Automatic test case data loading based on test function names

## Project Structure

```
AppiumAutomation/
├── config/
│   ├── app_config.json          # Default configuration file
│   ├── app_config_android.json  # Android-specific configuration
│   └── app_config_ios.json      # iOS-specific configuration
├── src/
│   ├── pages/                   # Page Object Model classes
│   │   ├── base_page.py         # Base page class
│   │   ├── login_page.py        # Example login page
│   │   └── home_page.py         # Example home page
│   ├── tests/                   # Test cases
│   │   ├── base_test.py         # Base test class
│   │   └── test_login.py        # Example test cases
│   └── utils/                   # Utility classes
│       ├── config_loader.py     # Configuration loader
│       ├── appium_wrapper.py    # Custom Appium wrapper
│       └── wait_utils.py        # Wait utilities
├── screenshots/                 # Screenshot storage (auto-created)
├── test_data/                   # Test data files (JSON)
│   ├── login_test_data.json     # Login test scenarios
│   └── user_test_data.json      # User management scenarios
├── pyproject.toml               # UV project configuration
├── requirements.txt             # Python dependencies (for pip users, optional if using uv)
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- [UV](https://github.com/astral-sh/uv) - Fast Python package installer
- Appium Server
- For Android: Android SDK, Java JDK
- For iOS: Xcode, iOS Simulator (macOS only)

### Setup with UV

1. Install UV (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install project dependencies:
```bash
uv sync
```

This will create a virtual environment and install all dependencies.

3. Activate the virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### Alternative: Traditional pip Installation

If you prefer using pip instead of uv:
```bash
pip install -r requirements.txt
```

**Note:** `requirements.txt` is optional if you're using `uv`. All dependencies are defined in `pyproject.toml`. The `requirements.txt` file is provided for compatibility with pip-based workflows.

### Appium Server Setup

1. Install Appium Server:
```bash
npm install -g appium
```

2. Install Appium drivers:
```bash
# For Android
appium driver install uiautomator2

# For iOS (macOS only)
appium driver install xcuitest
```

3. Start Appium Server:
```bash
appium
```

## Configuration

The framework supports both iOS and Android platforms. You can configure them in three ways:

### Method 1: Platform-Specific Config Files (Recommended)

Use separate configuration files for each platform:

- `config/app_config_android.json` - Android configuration
- `config/app_config_ios.json` - iOS configuration

### Method 2: Environment Variable

Set the `APPIUM_PLATFORM` environment variable:

```bash
# For Android
export APPIUM_PLATFORM=Android
python -m unittest discover -s src/tests

# For iOS
export APPIUM_PLATFORM=iOS
python -m unittest discover -s src/tests
```

### Method 3: Class Attribute

Set platform in your test class:

```python
class TestMyFeature(BaseTest):
    platform = "Android"  # or "iOS"
    
    def test_something(self):
        # Your test code
        pass
```

### Android Configuration Example

Edit `config/app_config_android.json`:

```json
{
  "app": {
    "build_number": "1.0.0",
    "version": "1.0",
    "package_name": "com.example.app",
    "activity_name": "com.example.app.MainActivity",
    "app_path": "./apps/app.apk"
  },
  "environment": {
    "platform": "Android",
    "platform_version": "11.0",
    "device_name": "emulator-5554",
    "automation_name": "UiAutomator2",
    "server_url": "http://localhost:4723",
    "android_capabilities": {
      "avd": "Pixel_4_API_30",
      "avdLaunchTimeout": 120000
    }
  },
  "capabilities": {
    "new_command_timeout": 300,
    "no_reset": false,
    "auto_grant_permissions": true
  }
}
```

### iOS Configuration Example

Edit `config/app_config_ios.json`:

```json
{
  "app": {
    "build_number": "1.0.0",
    "version": "1.0",
    "bundle_id": "com.example.app",
    "app_path": "./apps/app.ipa"
  },
  "environment": {
    "platform": "iOS",
    "platform_version": "16.0",
    "device_name": "iPhone 14",
    "automation_name": "XCUITest",
    "server_url": "http://localhost:4723",
    "ios_capabilities": {
      "udid": "",
      "xcodeOrgId": "",
      "xcodeSigningId": "iPhone Developer"
    }
  },
  "capabilities": {
    "new_command_timeout": 300,
    "no_reset": false,
    "autoAcceptAlerts": true
  }
}
```

## Usage

### Creating a Page Object

All page objects should inherit from `BasePage`:

```python
from src.pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class MyPage(BasePage):
    # Define locators
    BUTTON = (AppiumBy.ID, "com.example.app:id/button")
    
    def is_page_loaded(self) -> bool:
        """Override to check if page is loaded."""
        return self.appium.is_element_visible(self.BUTTON, timeout=5)
    
    def click_button(self):
        """Page-specific methods."""
        self.appium.click(self.BUTTON)
```

**Note:** Page objects automatically wait for page load in the constructor. You don't need to call `wait_for_page_load()` explicitly. To disable this behavior, use `MyPage(driver, wait_for_load=False)`.

### Writing Tests

With pytest, you use **fixtures** instead of inheriting from a base class. The framework provides these fixtures:

- `driver`: Appium WebDriver instance (created per test, resets app before each test)
- `appium_wrapper`: AppiumWrapper instance
- `wait_utils`: WaitUtils instance
- `test_data_loader`: TestDataLoader instance (for manual test data loading)
- `test_case`: Automatically loads test case data based on test function name
- `config`: Configuration dictionary

#### Simple Test Example:

```python
import pytest
from src.pages.my_page import MyPage

def test_something(driver):
    """Simple test using driver fixture."""
    # Page objects automatically wait for page load in constructor
    my_page = MyPage(driver)
    
    # Perform actions
    my_page.click_button()
    
    # Assertions
    assert my_page.is_page_loaded()
```

#### Test with Test Case Data (Implicit Loading):

```python
def test_successful_login(driver, test_case):
    """Test automatically loads test case data based on function name."""
    # test_case fixture automatically loads data for "test_successful_login"
    # Maps to "valid_login" test case in login_test_data.json
    
    login_page = LoginPage(driver)  # Automatically waits for page load
    home_page = login_page.login(
        test_case["username"], 
        test_case["password"]
    )  # Returns HomePage (automatically waits for page load)
    
    assert home_page.is_logged_in()
```

#### Test with Multiple Fixtures:

```python
def test_with_wrapper(driver, appium_wrapper, test_data_loader):
    """Test using multiple fixtures."""
    # Use appium_wrapper for direct operations
    appium_wrapper.click((AppiumBy.ID, "button_id"))
    
    # Load test data manually if needed
    test_data = test_data_loader.get_test_case_data("my_test_data", "test_case_1")
```

#### Data-Driven Test with Parametrize:

```python
@pytest.mark.parametrize("username,password,expected", [
    ("user1", "pass1", "success"),
    ("user2", "pass2", "error"),
    ("", "", "error"),
])
def test_login_scenarios(driver, username, password, expected):
    """Parametrized test - runs once for each parameter set."""
    login_page = LoginPage(driver)
    login_page.login(username, password)
    # Verify expected result...
```

#### Using Test Markers:

```python
@pytest.mark.smoke
def test_critical_feature(driver):
    """Marked as smoke test."""
    pass

@pytest.mark.android
def test_android_specific(driver):
    """Android-specific test."""
    pass
```

### Running Tests

The framework uses **pytest** for testing, which provides better fixtures, parametrization, and test organization.

#### Run all tests:
```bash
# Using UV (recommended)
uv run pytest

# Or with activated virtual environment
pytest
```

#### Run tests for a specific platform:
```bash
# Android
APPIUM_PLATFORM=Android uv run pytest

# iOS
APPIUM_PLATFORM=iOS uv run pytest
```

#### Run specific tests:
```bash
# Run a specific test file
uv run pytest src/tests/test_login.py

# Run a specific test function
uv run pytest src/tests/test_login.py::test_successful_login

# Run tests matching a pattern
uv run pytest -k "login"
```

#### Run tests with markers:
```bash
# Run only smoke tests
uv run pytest -m smoke

# Run only Android tests
uv run pytest -m android

# Run tests excluding regression
uv run pytest -m "not regression"
```

#### Generate HTML report:
```bash
uv run pytest --html=report.html --self-contained-html
```

#### Verbose output:
```bash
uv run pytest -v
```

## Data-Driven Testing

The framework supports data-driven testing by separating test data from test code. Test data is stored in JSON files in the `test_data/` directory.

### Test Data Structure

Test data files follow this structure:

```json
{
  "common": {
    "shared_data": "value"
  },
  "environments": {
    "default": {
      "base_url": "https://api.example.com"
    },
    "dev": {
      "base_url": "https://dev-api.example.com"
    }
  },
  "test_cases": {
    "test_case_name": {
      "field1": "value1",
      "field2": "value2",
      "expected_result": "success"
    }
  }
}
```

### Using Test Data in Tests

#### Method 1: Automatic Test Case Loading (Recommended)

The `test_case` fixture automatically loads test case data based on your test function name:

```python
def test_successful_login(driver, test_case):
    """Test automatically loads 'valid_login' test case."""
    # test_case is automatically loaded based on function name
    # test_successful_login -> valid_login (automatic mapping)
    
    login_page = LoginPage(driver)  # Automatically waits for page load
    home_page = login_page.login(
        test_case["username"], 
        test_case["password"]
    )  # Returns HomePage (automatically waits for page load)
    
    # Verify expected result
    if "expected_message" in test_case:
        assert test_case["expected_message"] in home_page.get_welcome_message()
```

**Automatic Test Name Mapping:**
- `test_successful_login` → `valid_login`
- `test_login_with_invalid_credentials` → `invalid_username`
- `test_login_with_empty_fields` → `empty_credentials`

**Override mapping if needed:**
```python
@pytest.mark.test_case_name("custom_test_case", data_file="my_test_data")
def test_custom(driver, test_case):
    # Uses custom_test_case from my_test_data.json
    pass
```

#### Method 2: Manual Test Case Loading

```python
def test_successful_login(driver, test_data_loader):
    """Test using manual test case data loading."""
    # Get specific test case data manually
    test_case = test_data_loader.get_test_case_data(
        "login_test_data", 
        "valid_login"
    )
    
    # Use test data
    login_page = LoginPage(driver)
    home_page = login_page.login(
        test_case["username"], 
        test_case["password"]
    )
    
    # Verify expected result
    if "expected_message" in test_case:
        assert test_case["expected_message"] in home_page.get_welcome_message()
```

#### Method 3: Data-Driven Test with Pytest Parametrize

```python
@pytest.mark.parametrize("test_case_name", [
    "valid_login",
    "invalid_username",
    "empty_credentials",
])
def test_login_scenarios(driver, test_data_loader, test_case_name):
    """Parametrized test - runs once for each test case."""
    # Get test case data
    test_case = test_data_loader.get_test_case_data("login_test_data", test_case_name)
    
    # Use test_case data
    login_page = LoginPage(driver)  # Automatically waits for page load
    home_page = login_page.login(
        test_case["username"],
        test_case["password"]
    )  # Returns HomePage (automatically waits for page load)
    # Verify results...
```

#### Method 4: Load All Test Cases Dynamically

```python
def test_all_login_scenarios(driver, test_data_loader):
    """Run all test cases from data file."""
    test_cases = test_data_loader.get_all_test_cases("login_test_data")
    
    for test_case in test_cases:
        test_name = test_case.get("_name", "unknown")
        login_page = LoginPage(driver)  # Automatically waits for page load
        # Use test_case data...
```

#### Method 4: Get Common Data

```python
def test_with_common_data(driver, test_data_loader):
    """Test using common/shared data."""
    # Get shared/common data
    common_data = test_data_loader.get_common_data("login_test_data")
    timeout = common_data.get("timeout", 30)
    # Use common data...
```

#### Method 5: Get Environment-Specific Data

```python
def test_with_env_data(driver, test_data_loader):
    """Test using environment-specific data."""
    # Get environment-specific data
    env_data = test_data_loader.get_environment_data(
        "login_test_data",
        environment="dev"  # or use TEST_ENV env variable
    )
    base_url = env_data.get("base_url")
    # Use env data...
```

### Test Data Loader Methods

- `load_test_data(filename)`: Load entire test data file
- `get_test_case_data(filename, test_case_name)`: Get specific test case
- `get_all_test_cases(filename)`: Get all test cases as a list
- `get_common_data(filename)`: Get common/shared data
- `get_environment_data(filename, environment)`: Get environment-specific data
- `clear_cache()`: Clear cached test data

### Example Test Data Files

- `test_data/login_test_data.json`: Login test scenarios
- `test_data/user_test_data.json`: User management test scenarios

## Framework Components

### Pytest Fixtures (conftest.py)
The framework provides pytest fixtures for easy test setup:

- **`driver` fixture**: Creates Appium driver, resets app before each test, quits after test
- **`appium_wrapper` fixture**: Provides AppiumWrapper instance
- **`wait_utils` fixture**: Provides WaitUtils instance
- **`test_data_loader` fixture**: Provides TestDataLoader instance (for manual data loading)
- **`test_case` fixture**: Automatically loads test case data based on test function name
- **`config` fixture**: Provides configuration dictionary

### BaseTest (Optional)
- Abstract base class for compatibility
- With pytest, you typically don't need to inherit from a base class
- Use fixtures directly in your test functions instead

### TestDataLoader
Utility for loading and managing test data:
- Load test data from JSON files
- Get specific test cases or all test cases
- Access common and environment-specific data
- Cache loaded data for performance

### AppiumWrapper
Custom wrapper providing:
- Element finding with explicit waits
- Element interactions (click, send_keys, etc.)
- Appium-specific methods (swipe, scroll, etc.)
- Screenshot capabilities

### WaitUtils
Explicit wait utilities:
- `wait_for_element_present()`
- `wait_for_element_visible()`
- `wait_for_element_clickable()`
- `wait_for_text_in_element()`
- Custom condition waits

### ConfigLoader
Loads and provides access to:
- App configuration (build, version, package)
- Environment configuration (platform, device)
- Capabilities configuration

## Best Practices

1. **Always use explicit waits**: Never use implicit waits. Use `WaitUtils` or `AppiumWrapper` methods.

2. **Page Object Model**: Keep all page-specific logic in page objects, not in tests.

3. **Use Pytest Fixtures**: Use the provided fixtures (`driver`, `test_case`, `appium_wrapper`, etc.) instead of inheriting from BaseTest.

4. **Use AppiumWrapper**: Use the custom wrapper instead of direct driver calls for consistency.

5. **Override `is_page_loaded()`**: Implement page-specific load checks in page objects. Page objects automatically wait for page load in the constructor.

6. **Use `test_case` fixture**: For automatic test case data loading based on test function names, use the `test_case` fixture instead of manually calling `test_data_loader.get_test_case_data()`.

7. **Configuration**: Use platform-specific config files or environment variables for easy platform switching.

8. **Platform Selection**: The framework automatically detects the platform from:
   - Class attribute `platform`
   - Environment variable `APPIUM_PLATFORM`
   - Configuration file name (`app_config_android.json` or `app_config_ios.json`)
   - Default config file platform setting

9. **Data-Driven Testing**: Use test data files to separate test logic from test data:
   - Store test data in JSON files in `test_data/` directory
   - Use `test_case` fixture for automatic test case loading based on test function names
   - Use `test_data_loader` for manual test data access when needed
   - Support for common data, environment-specific data, and test cases

## Platform-Specific Notes

### Android
- Requires `package_name` and optionally `activity_name` in config
- Uses `UiAutomator2` automation by default
- Supports AVD (Android Virtual Device) configuration
- `auto_grant_permissions` capability is Android-specific

### iOS
- Requires `bundle_id` in config
- Uses `XCUITest` automation by default
- Requires Xcode and iOS Simulator (macOS only)
- `autoAcceptAlerts` and `autoDismissAlerts` are iOS-specific
- May require code signing configuration for real devices

## General Notes

- The framework automatically resets the app before each test using `driver.reset()`
- All waits are explicit - no implicit waits are used
- Page objects automatically wait for page load in the constructor (no need to call `wait_for_page_load()` explicitly)
- Test case data is automatically loaded via the `test_case` fixture based on test function names
- Screenshots are automatically saved to the `screenshots/` directory
- The framework is designed to be easily extensible and maintainable
- Platform-specific capabilities are automatically applied based on the selected platform

