"""Configuration loader utility for reading JSON configuration files."""
import json
import os
from typing import Dict, Any, Optional


class ConfigLoader:
    """Loads and manages application configuration from JSON files."""
    
    def __init__(self, config_path: str = None, platform: str = None):
        """
        Initialize ConfigLoader.
        
        Args:
            config_path: Path to the JSON configuration file.
                        If None, uses default path based on platform or app_config.json.
            platform: Platform to use ("iOS" or "Android"). If None, reads from config or env.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        if config_path is None:
            # Check for platform-specific config or use default
            if platform:
                platform_lower = platform.lower()
                platform_config = os.path.join(project_root, "config", f"app_config_{platform_lower}.json")
                default_config = os.path.join(project_root, "config", "app_config.json")
                if os.path.exists(platform_config):
                    config_path = platform_config
                else:
                    config_path = default_config
            else:
                # Check environment variable for platform
                env_platform = os.getenv("APPIUM_PLATFORM", "").lower()
                if env_platform:
                    platform_config = os.path.join(project_root, "config", f"app_config_{env_platform}.json")
                    if os.path.exists(platform_config):
                        config_path = platform_config
                    else:
                        config_path = os.path.join(project_root, "config", "app_config.json")
                else:
                    config_path = os.path.join(project_root, "config", "app_config.json")
        
        self.config_path = config_path
        self._config = self._load_config()
        
        # Determine platform from config or parameter
        if platform:
            self._platform = platform
        else:
            self._platform = self.get_environment_config().get("platform", "Android")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def get_app_config(self) -> Dict[str, Any]:
        """Get app configuration section."""
        return self._config.get("app", {})
    
    def get_environment_config(self) -> Dict[str, Any]:
        """Get environment configuration section."""
        return self._config.get("environment", {})
    
    def get_capabilities_config(self) -> Dict[str, Any]:
        """Get capabilities configuration section."""
        return self._config.get("capabilities", {})
    
    def get_build_number(self) -> str:
        """Get app build number."""
        return self.get_app_config().get("build_number", "")
    
    def get_version(self) -> str:
        """Get app version."""
        return self.get_app_config().get("version", "")
    
    def get_environment(self) -> str:
        """Get environment name."""
        return self.get_environment_config().get("environment", "default")
    
    def get_platform(self) -> str:
        """Get the platform (iOS or Android)."""
        return self._platform
    
    def get_all_capabilities(self) -> Dict[str, Any]:
        """Get all capabilities merged together, platform-specific."""
        app_config = self.get_app_config()
        env_config = self.get_environment_config()
        caps_config = self.get_capabilities_config()
        platform = self.get_platform()
        
        # Base capabilities
        capabilities = {
            "platformName": platform,
            "platformVersion": env_config.get("platform_version", ""),
            "deviceName": env_config.get("device_name", ""),
            "app": app_config.get("app_path", ""),
            **caps_config
        }
        
        # Platform-specific capabilities
        if platform.lower() == "android":
            capabilities["automationName"] = env_config.get("automation_name", "UiAutomator2")
            # Android-specific
            if app_config.get("package_name"):
                capabilities["appPackage"] = app_config.get("package_name")
            if app_config.get("activity_name"):
                capabilities["appActivity"] = app_config.get("activity_name")
            # Android capabilities from config
            android_caps = env_config.get("android_capabilities", {})
            capabilities.update(android_caps)
            
        elif platform.lower() == "ios":
            capabilities["automationName"] = env_config.get("automation_name", "XCUITest")
            # iOS-specific
            if app_config.get("bundle_id"):
                capabilities["bundleId"] = app_config.get("bundle_id")
            # iOS capabilities from config
            ios_caps = env_config.get("ios_capabilities", {})
            capabilities.update(ios_caps)
        
        return capabilities
    
    def get_server_url(self) -> str:
        """Get Appium server URL."""
        return self.get_environment_config().get("server_url", "http://localhost:4723")

