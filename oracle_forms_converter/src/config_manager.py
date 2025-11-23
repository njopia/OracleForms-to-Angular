"""
Configuration Manager
Handles saving and loading of configuration settings
"""
import json
import os
from pathlib import Path


class ConfigManager:
    def __init__(self):
        self.config_file = self._get_config_file_path()
        self.config = self._load_config()

    def _get_config_file_path(self):
        """Get the configuration file path"""
        # Store config in the config directory
        config_dir = Path(__file__).parent.parent / 'config'
        config_dir.mkdir(exist_ok=True)
        return config_dir / 'settings.json'

    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()

    def _get_default_config(self):
        """Get default configuration"""
        # Try to detect Oracle Home from environment
        oracle_home = os.environ.get('ORACLE_HOME', '')

        # Try to detect Java Home
        java_home = os.environ.get('JAVA_HOME', '')

        # Default output directory
        output_dir = str(Path(__file__).parent.parent / 'output')

        return {
            'oracle_home': oracle_home,
            'java_home': java_home,
            'output_dir': output_dir,
            'recent_files': [],
            'last_input_dir': '',
            'auto_open_output': True
        }

    def save_config(self, oracle_home, java_home, output_dir):
        """Save configuration to file"""
        self.config['oracle_home'] = oracle_home
        self.config['java_home'] = java_home
        self.config['output_dir'] = output_dir

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_oracle_home(self):
        """Get Oracle Home path"""
        return self.config.get('oracle_home', '')

    def get_java_home(self):
        """Get Java Home path"""
        return self.config.get('java_home', '')

    def get_output_dir(self):
        """Get output directory path"""
        return self.config.get('output_dir', '')

    def add_recent_file(self, file_path):
        """Add file to recent files list"""
        recent = self.config.get('recent_files', [])

        # Remove if already exists
        if file_path in recent:
            recent.remove(file_path)

        # Add to beginning
        recent.insert(0, file_path)

        # Keep only last 10
        self.config['recent_files'] = recent[:10]

        # Save
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except:
            pass

    def get_recent_files(self):
        """Get recent files list"""
        return self.config.get('recent_files', [])

    def set_last_input_dir(self, directory):
        """Set last used input directory"""
        self.config['last_input_dir'] = directory
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except:
            pass

    def get_last_input_dir(self):
        """Get last used input directory"""
        return self.config.get('last_input_dir', '')
