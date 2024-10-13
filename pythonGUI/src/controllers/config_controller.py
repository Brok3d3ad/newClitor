import configparser
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ConfigController:
    def __init__(self, config_file_path):
        # Store the path to the config file, handling development and PyInstaller modes
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()

    def read_value(self, section, key, fallback=None):
        """Reads a value from the config file. If the file doesn't exist, raises an error."""
        if os.path.exists(self.config_file_path):
            # Read the config file
            self.config.read(self.config_file_path)
            # Return the requested value, or the fallback if the key doesn't exist
            return self.config.get(section, key, fallback=fallback)
        else:
            raise FileNotFoundError(f"Config file not found: {self.config_file_path}")

    def write_value(self, section, key, value):
        """Writes a key-value pair to the config file in the specified section."""
        # Ensure the config file exists and the section exists
        if os.path.exists(self.config_file_path):
            self.config.read(self.config_file_path)
        if not self.config.has_section(section):
            self.config.add_section(section)

        # Set the key-value pair in the section
        self.config.set(section, key, value)

        # Write the changes back to the config file
        with open(self.config_file_path, 'w') as configfile:
            self.config.write(configfile)

    def reset_to_default(self, section, key, default_value):
        """Resets a specific key in the section to a default value."""
        if os.path.exists(self.config_file_path):
            self.config.read(self.config_file_path)
            
            if self.config.has_section(section) and self.config.has_option(section, key):
                # Set the key to the default value
                self.config.set(section, key, default_value)
                
                # Write changes to the config file
                with open(self.config_file_path, 'w') as configfile:
                    self.config.write(configfile)
        else:
            raise FileNotFoundError(f"Config file not found: {self.config_file_path}")

