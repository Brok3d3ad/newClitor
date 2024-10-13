import tkinter as tk
from tkinter import messagebox
from gui.image_loader import load_icon, load_background_image
from controllers.config_controller import ConfigController


class TestToggleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MZ Clitor")
        self.root.geometry('250x100')
        self.root.config(bg='#1a1e22')

        # Initialize the ConfigController with the path to the config file
        self.config_controller = ConfigController('pythonGUI\config\config.ini')

        # Load the file paths from the [Paths] section of config.ini
        self.icon_path = self.config_controller.read_value('Paths', 'ICON_PATH')
        self.background_image_path = self.config_controller.read_value('Paths', 'BACKGROUND_IMAGE_PATH')
        self.config_file_path = self.config_controller.read_value('Paths', 'CONFIG_FILE_PATH')
        # Dictionary to store the test variables and their labels
        self.test_vars = {}
        self.test_labels = {}
        self.frames = []

        # Create initial layout by adding some default variables
        self.create_widgets()

        # Initially arrange the widgets after they are created
        self.rearrange_widgets(None)

        # Bind the window resizing event to rearrange elements dynamically
        self.root.bind("<Configure>", self.rearrange_widgets)

    def create_widgets(self):
        """Initial function to add some default variables."""
        # Add variables by reading from config or setting defaults
        var1 = "ilunya"
        var2 = "mashasha"
        self.add_variable(var1, self.config_controller.read_value('default', var1, fallback="0"))  # Default value: OFF
        self.add_variable(var2, self.config_controller.read_value('default', var2, fallback="0"))  # Default value: ON

    def add_variable(self, variable_name, initial_value="0"):
        """Adds a new variable with a toggle button and ON/OFF label."""
        # Create a new frame for this variable
        frame = tk.Frame(self.root, bg='#1a1e22')
        frame.grid_columnconfigure(0, weight=0,minsize=100)
        frame.grid_columnconfigure(1, weight=0)
        frame.grid_columnconfigure(2, weight=0)

        # Label to display the variable name
        variable_label = tk.Label(frame, text=variable_name.capitalize(), font=('Helvetica', 12), fg='#fbfbfb', bg='#1a1e22')
        variable_label.grid(row=0, column=0, sticky='w', padx=(0, 0))

        # Button to toggle the variable value
        toggle_button = tk.Button(frame, text="Toggle", command=lambda: self.toggle_variable(variable_name), fg='#fbfbfb', bg='#1a1e22')
        toggle_button.grid(row=0, column=1, sticky='w', padx=(0, 0))  # Reduced padding on the right side

        # Label to display the current value (ON/OFF) with a fixed width
        value_label = tk.Label(frame, text=initial_value, font=('Helvetica', 12, 'bold'), bg='#1a1e22', fg='#fbfbfb', width=4)
        value_label.grid(row=0, column=2, sticky='w', padx=(0, 0))  # Reduced padding on the left side

        # Store the frame and label for dynamic reconfiguration
        self.frames.append(frame)
        self.test_labels[variable_name] = value_label
        self.test_vars[variable_name] = tk.StringVar(value=initial_value)

        # Set initial value and display color
        self.update_variable_display(variable_name, initial_value)

    def toggle_variable(self, variable_name):
        """Toggles the value of the variable between ON and OFF."""
        current_value = self.test_vars[variable_name].get()
        new_value = '1' if current_value == '0' else '0'
        self.test_vars[variable_name].set(new_value)
        self.update_variable_display(variable_name, new_value)

        # Update the config with the new value using ConfigController
        self.config_controller.write_value('default', variable_name, new_value)

    def update_variable_display(self, variable_name, value):
        """Updates the display of the variable to show 'ON' in green or 'OFF' in red."""
        if value == '1':
            self.test_labels[variable_name].config(text='ON', fg='#1bc454')  # Green for ON
        else:
            self.test_labels[variable_name].config(text='OFF', fg='#cd2d1b')  # Red for OFF

    def rearrange_widgets(self, event):
        """Dynamically rearrange the widgets into a grid based on window size."""
        width = self.root.winfo_width()  # Get the current width of the window
        columns = max(1, width // 200)  # Adjust the number of columns based on window width (200px per column)

        for index, frame in enumerate(self.frames):
            row = index // columns
            column = index % columns
            frame.grid(row=row, column=column, padx=10, pady=5, sticky='ew')

        # Make sure each column can expand
        for i in range(columns):
            self.root.grid_columnconfigure(i, weight=1)

        # Make sure rows can expand
        for i in range((len(self.frames) + columns - 1) // columns):
            self.root.grid_rowconfigure(i, weight=1)
        """Dynamically rearrange the widgets into a grid based on window size."""
        width = self.root.winfo_width()  # Get the current width of the window
        columns = max(1, width // 200)  # Adjust the number of columns based on window width (200px per column)

        for index, frame in enumerate(self.frames):
            row = index // columns
            column = index % columns
            frame.grid(row=row, column=column, padx=10, pady=5, sticky='ew')

        # Make sure each column can expand
        for i in range(columns):
            self.root.grid_columnconfigure(i, weight=1)

        # Make sure rows can expand
        for i in range((len(self.frames) + columns - 1) // columns):
            self.root.grid_rowconfigure(i, weight=1)