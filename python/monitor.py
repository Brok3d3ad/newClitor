import tkinter as tk
from tkinter import font
from tkinter import ttk
import configparser
import time
from pathlib import Path
from PIL import Image, ImageTk

class MonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Monitor")
        self.root.configure(bg='#1E1E1E')
        
        # Make window transparent and always on top
        self.root.attributes('-alpha', 0.8)  # 80% opacity (0.0 to 1.0)
        self.root.attributes('-topmost', True)  # Always on top
        
        # Add bindings for window dragging
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)
        
        # Make window freely resizable and set smaller minimum size
        self.root.resizable(True, True)
        
        # Create control frame with only close button
        size_control_frame = ttk.Frame(root, style='Monitor.TFrame')
        size_control_frame.grid(row=0, column=1, sticky='ne', padx=5, pady=2)
        
        close_button = ttk.Label(size_control_frame, text="×", style='CloseButton.TLabel')
        close_button.pack(side='left', padx=2)
        close_button.bind('<Button-1>', lambda e: root.destroy())
        
        # Add button styles
        style = ttk.Style()
        style.configure('CloseButton.TLabel',
                       background='#1E1E1E',
                       foreground='#AAAAAA',
                       font=('Segoe UI', 12, 'bold'))
        
        # Store original window size
        self.is_minimized = False
        self.original_size = None
        
        # Create main container frame with smaller padding
        main_frame = ttk.Frame(root, style='Monitor.TFrame')
        main_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=2, pady=2)  # Updated row and columnspan
        
        # Configure root grid
        root.grid_columnconfigure(0, weight=1)
        
        # Style configuration for more compact layout
        style = ttk.Style()
        style.configure('Monitor.TFrame', background='#1E1E1E')
        style.configure('Monitor.TLabel', 
                       background='#1E1E1E',
                       foreground='#00FF00',
                       font=('Segoe UI', 12, 'bold'),  # Increased font size
                       padding=2)  # Reduced padding
        
        # Create frames for each character with compact layout
        self.char_labels = {}
        
        # Load all images at initialization
        self.images = {}
        self.load_images()
        
        # Store initial font sizes with fixed value
        self.default_font_size = 15  # Fixed size to match image height
        self.current_font_size = self.default_font_size
        
        # Style configuration with fixed font size
        style = ttk.Style()
        style.configure('Monitor.TFrame', background='#1E1E1E')
        style.configure('Monitor.TLabel', 
                       background='#1E1E1E',
                       foreground='#00FF00',
                       font=('Segoe UI', self.default_font_size, 'bold'),
                       padding=2)
        
        # Create labels with consistent spacing and sizing
        for char_num in range(1, 6):
            section = f"Character{char_num}"
            frame = ttk.Frame(self.root, style='Monitor.TFrame')
            frame.grid(row=char_num-1, column=0, sticky='w', padx=2, pady=1)
            
            self.char_labels[section] = {}
            
            # Name label with smaller width
            name_label = ttk.Label(frame, style='Monitor.TLabel', width=10)  # Reduced from 15 to 10
            name_label.grid(row=0, column=0, sticky='w', padx=(2,5))
            self.char_labels[section]['name'] = name_label
            
            # HP label with fixed width
            hp_label = ttk.Label(frame, style='Monitor.TLabel', width=8)  # Fixed width for "ХП: 100"
            hp_label.grid(row=0, column=1, sticky='w', padx=(2,2))
            self.char_labels[section]['hp'] = hp_label
            
            # Energy label with fixed width
            energy_label = ttk.Label(frame, style='Monitor.TLabel', width=12)  # Fixed width for "Энергия: 100"
            energy_label.grid(row=0, column=2, sticky='w', padx=(2,5))
            self.char_labels[section]['energy'] = energy_label
            
            # Status icons - all with consistent padding
            auto_shoot = ttk.Label(frame, style='Monitor.TLabel')
            auto_shoot.grid(row=0, column=3, sticky='w', padx=2)
            self.char_labels[section]['auto_shoot'] = auto_shoot
            
            auto_aim = ttk.Label(frame, style='Monitor.TLabel')
            auto_aim.grid(row=0, column=4, sticky='w', padx=2)
            self.char_labels[section]['auto_aim'] = auto_aim
            
            invite = ttk.Label(frame, style='Monitor.TLabel')
            invite.grid(row=0, column=5, sticky='w', padx=2)
            self.char_labels[section]['invite'] = invite
            
            auto_pick_up = ttk.Label(frame, style='Monitor.TLabel')
            auto_pick_up.grid(row=0, column=6, sticky='w', padx=2)
            self.char_labels[section]['auto_pick_up'] = auto_pick_up
            
            auto_hp_regen = ttk.Label(frame, style='Monitor.TLabel')
            auto_hp_regen.grid(row=0, column=7, sticky='w', padx=2)
            self.char_labels[section]['auto_hp_regen'] = auto_hp_regen
            
            auto_energy_regen = ttk.Label(frame, style='Monitor.TLabel')
            auto_energy_regen.grid(row=0, column=8, sticky='w', padx=2)
            self.char_labels[section]['auto_energy_regen'] = auto_energy_regen
            
            insurance = ttk.Label(frame, style='Monitor.TLabel')
            insurance.grid(row=0, column=9, sticky='w', padx=2)
            self.char_labels[section]['insurance'] = insurance
        
        # Start updating values
        self.update_values()
        
        # Remove or comment out the on_window_resize binding
        # self.root.bind('<Configure>', self.on_window_resize)
        
    def update_font_style(self):
        style = ttk.Style()
        style.configure('Monitor.TLabel', 
                       background='#1E1E1E',
                       foreground='#00FF00',
                       font=('Segoe UI', self.current_font_size, 'bold'),
                       padding=2)
    
    def on_window_resize(self, event):
        # Only process if this is a root window event
        if event.widget == self.root:
            # Get the current window width
            window_width = self.root.winfo_width()
            
            # Calculate required width for text (approximate)
            required_width = 160 * self.current_font_size  # Doubled from 80 to 160 for larger text
            
            # Adjust font size if needed
            if required_width > window_width and self.current_font_size > 8:  # Changed minimum from 4 to 8
                self.current_font_size -= 1
                self.update_font_style()
            elif required_width < window_width * 0.8 and self.current_font_size < self.default_font_size:
                self.current_font_size += 1
                self.update_font_style()
            
            # Update all existing labels with new font
            for char_labels in self.char_labels.values():
                for label in char_labels.values():
                    label.configure(style='Monitor.TLabel')
    
    def update_values(self):
        config = configparser.ConfigParser()
        config_path = Path(__file__).parent / 'config.ini'
        config.read(config_path)
    
        for char_num in range(1, 6):
            section = f"Character{char_num}"
            if section in config:
                # Name with shorter ellipsis
                name = config[section].get('name', f'Character {char_num}')
                if len(name) > 10:  # Reduced from 15 to 10
                    name = name[:7] + "..."  # Adjusted to match new width
                self.char_labels[section]['name'].config(
                    text=f"{name}",
                    foreground='#4A9EFF')
                
                try:
                    # HP and Energy with Russian text
                    hp = int(config[section].get('hp_level', '0'))
                    hp_color = '#FF4444' if hp < 20 and int(time.time() * 2) % 2 else '#00FF44'
                    self.char_labels[section]['hp'].config(
                        text=f"ХП: {hp:3d}",  # HP in Russian
                        foreground=hp_color)
                    
                    energy = int(config[section].get('energy_level', '0'))
                    energy_color = '#FF4444' if energy < 20 and int(time.time() * 2) % 2 else '#00FF44'
                    self.char_labels[section]['energy'].config(
                        text=f"Энергия: {energy:3d}",  # Energy in Russian
                        foreground=energy_color)
                    
                    # Status icons
                    states = {
                        'auto_shoot': 'auto_shoot_state',
                        'auto_aim': 'auto_aim_state',
                        'auto_pick_up': 'auto_pick_up_state',
                        'auto_hp_regen': 'auto_hp_regen_state',
                        'auto_energy_regen': 'auto_energy_regen_state'
                    }
                    
                    for label_key, config_key in states.items():
                        state = "on" if int(config[section].get(config_key, '0')) else "off"
                        self.char_labels[section][label_key].config(
                            image=self.images[f'{label_key}_{state}'],
                            text="")
                    
                    # Insurance with blinking when off
                    insurance = int(config[section].get('insurance_state', '0'))
                    if insurance:
                        self.char_labels[section]['insurance'].config(
                            image=self.images['insurance_on'],
                            text="")
                    else:
                        # Blink insurance icon when off
                        blink = int(time.time() * 2) % 2
                        self.char_labels[section]['insurance'].config(
                            image=self.images['insurance_off'] if blink else "",
                            text="")
                    
                    # Update invite with on/off image
                    invite = "on" if int(config[section].get('invite_state', '0')) else "off"
                    self.char_labels[section]['invite'].config(
                        image=self.images[f'invite_{invite}'],
                        text="")

                except (ValueError, KeyError) as e:
                    print(f"Error updating values for {section}: {e}")
    
        # Schedule next update
        self.root.after(100, self.update_values)
        
    # Add these new methods for window dragging
    def start_move(self, event):
        self.x = event.x_root
        self.y = event.y_root

    def on_move(self, event):
        deltax = event.x_root - self.x
        deltay = event.y_root - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        self.x = event.x_root
        self.y = event.y_root

    def increase_size(self, event):
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()
        new_width = int(current_width * 1.2)
        new_height = int(current_height * 1.2)
        self.root.geometry(f"{new_width}x{new_height}")

    def decrease_size(self, event):
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()
        new_width = max(100, int(current_width * 0.8))  # Reduced minimum size to 100
        new_height = max(100, int(current_height * 0.8))  # Reduced minimum size to 100
        self.root.geometry(f"{new_width}x{new_height}")

    def load_images(self):
        """Load all images and store them in self.images dictionary"""
        image_path = Path(__file__).parent / 'images'
        
        try:
            # Function to resize images
            def load_and_resize(path, scale=1.5):
                img = Image.open(path)
                new_size = (int(img.width * scale), int(img.height * scale))
                return ImageTk.PhotoImage(img.resize(new_size, Image.Resampling.LANCZOS))

            # Load and resize all images
            top_right = image_path / 'top_right_panel'
            self.images.update({
                'auto_shoot_on': load_and_resize(top_right / 'auto_shoot_on.bmp'),
                'auto_shoot_off': load_and_resize(top_right / 'auto_shoot_off.bmp'),
                'auto_aim_on': load_and_resize(top_right / 'auto_aim_on.bmp'),
                'auto_aim_off': load_and_resize(top_right / 'auto_aim_off.bmp'),
                'auto_pick_up_on': load_and_resize(top_right / 'auto_pick_up_on.bmp'),
                'auto_pick_up_off': load_and_resize(top_right / 'auto_pick_up_off.bmp'),
                'auto_hp_regen_on': load_and_resize(top_right / 'auto_hp_regen_on.bmp'),
                'auto_hp_regen_off': load_and_resize(top_right / 'auto_hp_regen_off.bmp'),
                'auto_energy_regen_on': load_and_resize(top_right / 'auto_energy_regen_on.bmp'),
                'auto_energy_regen_off': load_and_resize(top_right / 'auto_energy_regen_off.bmp'),
            })
            
            map_block = image_path / 'map_block'
            self.images.update({
                'insurance_on': load_and_resize(map_block / 'insurance_on.bmp'),
                'insurance_off': load_and_resize(map_block / 'insurance_off.bmp'),
            })
            
            top_left = image_path / 'top_left_actions_panel'
            self.images.update({
                'invite_on': load_and_resize(top_left / 'invite_on.bmp'),
                'invite_off': load_and_resize(top_left / 'invite_off.bmp'),
            })
            
        except FileNotFoundError as e:
            print(f"Error loading images: {e}")
            print(f"Looking for images in: {image_path}")

def main():
    root = tk.Tk()
    
    # Optional: Remove window decorations for a cleaner look
    root.overrideredirect(True)
    
    app = MonitorGUI(root)
    
    # Update the window to calculate required size
    root.update()
    
    # Get the required size based on content
    required_width = root.winfo_reqwidth()
    required_height = root.winfo_reqheight()
    
    # Set the window size to exactly match the required size
    root.geometry(f"{required_width}x{required_height}")
    
    # Set minimum size to match the required size
    root.minsize(required_width, required_height)
    
    root.mainloop()

if __name__ == "__main__":
    main()
