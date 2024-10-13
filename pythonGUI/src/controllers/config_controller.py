import configparser
import os

class ConfigController:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)

    def read_value(self, section, key, fallback=None):
        """Read a value from the config file."""
        if os.path.exists(self.config_file_path):
            self.config.read(self.config_file_path)
            return self.config.get(section, key, fallback=fallback)
        else:
            raise FileNotFoundError(f"Config file not found: {self.config_file_path}")

    def write_value(self, section, key, value):
        """Write a value to the config file."""
        if not os.path.exists(self.config_file_path):
            raise FileNotFoundError(f"Config file not found: {self.config_file_path}")
        
        self.config.read(self.config_file_path)
        
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value

        with open(self.config_file_path, 'w') as configfile:
            self.config.write(configfile)

    def reset_to_default(self, section, key, default_value):
        """Reset a specific key in the 'default' section to its default value."""
        if not os.path.exists(self.config_file_path):
            raise FileNotFoundError(f"Config file not found: {self.config_file_path}")

        self.config.read(self.config_file_path)
        
        # Reset only the specified key to its default value if it exists
        if section in self.config and key in self.config[section]:
            self.config[section][key] = default_value

            with open(self.config_file_path, 'w') as configfile:
                self.config.write(configfile)
