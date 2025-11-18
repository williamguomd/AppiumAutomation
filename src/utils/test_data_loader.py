"""Test data loader utility for data-driven testing."""
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path


class TestDataLoader:
    """Loads and manages test data from JSON files."""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize TestDataLoader.
        
        Args:
            data_dir: Path to test data directory. If None, uses default path.
        """
        if data_dir is None:
            # Default to test_data directory relative to project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            data_dir = os.path.join(project_root, "test_data")
        
        self.data_dir = data_dir
        self._cache: Dict[str, Any] = {}
    
    def load_test_data(self, filename: str, cache: bool = True) -> Dict[str, Any]:
        """
        Load test data from a JSON file.
        
        Args:
            filename: Name of the JSON file (with or without .json extension)
            cache: Whether to cache the loaded data (default: True)
            
        Returns:
            Dictionary containing test data
            
        Raises:
            FileNotFoundError: If the test data file is not found
            ValueError: If the JSON is invalid
        """
        # Use cached data if available
        if cache and filename in self._cache:
            return self._cache[filename]
        
        # Add .json extension if not present
        if not filename.endswith('.json'):
            filename = f"{filename}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Test data file not found: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cache the data
            if cache:
                self._cache[filename] = data
            
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in test data file {filepath}: {e}")
    
    def get_test_case_data(self, filename: str, test_case_name: str) -> Dict[str, Any]:
        """
        Get specific test case data from a test data file.
        
        Args:
            filename: Name of the test data JSON file
            test_case_name: Name of the test case to retrieve
            
        Returns:
            Dictionary containing test case data
            
        Raises:
            KeyError: If test case name is not found
        """
        data = self.load_test_data(filename)
        
        if 'test_cases' not in data:
            raise ValueError(f"Test data file {filename} does not contain 'test_cases' key")
        
        if test_case_name not in data['test_cases']:
            raise KeyError(f"Test case '{test_case_name}' not found in {filename}")
        
        return data['test_cases'][test_case_name]
    
    def get_all_test_cases(self, filename: str) -> List[Dict[str, Any]]:
        """
        Get all test cases from a test data file.
        
        Args:
            filename: Name of the test data JSON file
            
        Returns:
            List of test case dictionaries
        """
        data = self.load_test_data(filename)
        
        if 'test_cases' not in data:
            return []
        
        test_cases = []
        for name, test_data in data['test_cases'].items():
            test_case = test_data.copy()
            test_case['_name'] = name  # Include test case name
            test_cases.append(test_case)
        
        return test_cases
    
    def get_common_data(self, filename: str) -> Dict[str, Any]:
        """
        Get common/shared data from a test data file.
        
        Args:
            filename: Name of the test data JSON file
            
        Returns:
            Dictionary containing common data (empty dict if not found)
        """
        data = self.load_test_data(filename)
        return data.get('common', {})
    
    def get_environment_data(self, filename: str, environment: str = None) -> Dict[str, Any]:
        """
        Get environment-specific data from a test data file.
        
        Args:
            filename: Name of the test data JSON file
            environment: Environment name (e.g., 'dev', 'staging', 'prod')
                        If None, uses 'default'
            
        Returns:
            Dictionary containing environment-specific data
        """
        data = self.load_test_data(filename)
        
        if environment is None:
            environment = os.getenv('TEST_ENV', 'default')
        
        env_data = data.get('environments', {}).get(environment, {})
        
        # Merge with default environment if exists
        if environment != 'default' and 'default' in data.get('environments', {}):
            default_env = data['environments']['default']
            merged = default_env.copy()
            merged.update(env_data)
            return merged
        
        return env_data
    
    def clear_cache(self):
        """Clear the test data cache."""
        self._cache.clear()
    
    def merge_data(self, base_data: Dict[str, Any], override_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two data dictionaries, with override_data taking precedence.
        
        Args:
            base_data: Base data dictionary
            override_data: Data to override base data
            
        Returns:
            Merged dictionary
        """
        merged = base_data.copy()
        merged.update(override_data)
        return merged

