import tkinter as tk
from tkinter import messagebox
import configparser
import os
from PIL import Image, ImageTk

class AutoattackToggleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("INI File Autoattack Toggle")
        self.root.geometry('400x400')  # Set the window size

        # Set the window icon (replace 'icon.png' with your icon file)

        self.icon_image = Image.open('pythonGUI\sigma.png')  # Replace with your image file
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        self.root.iconphoto(False, self.icon_photo)
        
        # Load the background image
        self.background_image = Image.open('pythonGUI\POGONA.gif')  # Replace with your image file
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create a label for the background image
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Make the label cover the entire window

        # Configuration file path
        self.config_file_path = 'pythonGUI\config.ini'

        # Variable to store the autoattack value
        self.autoattack_var = tk.StringVar()

        # Create the GUI components
        self.create_widgets()

        # Initialize by reading the current autoattack value
        self.read_autoattack_from_ini()

    def create_widgets(self):
        """Create and place the widgets in the window."""
        # Label to display the autoattack value
        self.autoattack_label = tk.Label(self.root, textvariable=self.autoattack_var, font=('Helvetica', 16), bg='#ffffff')
        self.autoattack_label.pack(padx=20, pady=20)

        # Button to toggle the autoattack value
        self.toggle_button = tk.Button(self.root, text="Toggle Autoattack", command=self.toggle_autoattack)
        self.toggle_button.pack(padx=20, pady=10)

    def read_autoattack_from_ini(self):
        """Read the autoattack value from the .ini file and update the display."""
        try:
            if os.path.exists(self.config_file_path):
                config = configparser.ConfigParser()
                config.read(self.config_file_path)
                autoattack_value = config.get('Settings', 'autoattack', fallback='0')
                self.autoattack_var.set(autoattack_value)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def toggle_autoattack(self):
        """Toggle the autoattack value in the .ini file and update the display."""
        try:
            # Check if the .ini file exists
            if not os.path.exists(self.config_file_path):
                messagebox.showerror("File Error", f"The file '{self.config_file_path}' was not found.")
                return

            # Read the current value from the ini file
            config = configparser.ConfigParser()
            config.read(self.config_file_path)

            # Check if the 'Settings' section exists, if not create it
            if 'Settings' not in config:
                config['Settings'] = {}

            # Toggle the autoattack value
            current_value = config.get('Settings', 'autoattack', fallback='0')
            new_value = '1' if current_value == '0' else '0'
            config['Settings']['autoattack'] = new_value

            # Write the updated configuration back to the file
            with open(self.config_file_path, 'w') as configfile:
                config.write(configfile)

            # Update the displayed autoattack value
            self.autoattack_var.set(new_value)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoattackToggleApp(root)
    root.mainloop()
