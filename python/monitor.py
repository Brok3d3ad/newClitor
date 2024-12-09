import tkinter as tk
from tkinter import font
from tkinter import ttk
import configparser
import time
from pathlib import Path

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
        self.root.minsize(200, 200)  # Reduced minimum size
        
        # Create close button in top-right corner
        close_button = ttk.Label(root, text="×", style='CloseButton.TLabel')
        close_button.grid(row=0, column=1, sticky='ne', padx=5, pady=2)
        close_button.bind('<Button-1>', lambda e: root.destroy())
        
        # Add close button style
        style = ttk.Style()
        style.configure('CloseButton.TLabel',
                       background='#1E1E1E',
                       foreground='#FF4444',
                       font=('Segoe UI', 12, 'bold'))
        
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
                       font=('Segoe UI', 10, 'bold'),  # Smaller font
                       padding=2)  # Reduced padding
        
        # Create frames for each character with compact layout
        self.char_labels = {}
        
        for i in range(5):
            char_num = i + 1
            
            char_frame = ttk.Frame(main_frame, style='Monitor.TFrame')
            char_frame.grid(row=i, column=0, sticky='nsew', padx=2, pady=1)  # Reduced padding
            
            # Configure char_frame grid
            char_frame.grid_columnconfigure(0, weight=1)
            
            # Stats container frame - now directly in row 0 instead of row 1
            stats_frame = ttk.Frame(char_frame, style='Monitor.TFrame')
            stats_frame.grid(row=0, column=0, sticky='nsew', pady=1)
            
            # Create labels for all config values
            name_label = ttk.Label(stats_frame, style='Monitor.TLabel')
            name_label.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=1, pady=0)
            
            # First row: HP and Energy
            hp_label = ttk.Label(stats_frame, width=8, style='Monitor.TLabel')
            hp_label.grid(row=1, column=0, sticky='nsew', padx=1, pady=0)
            
            energy_label = ttk.Label(stats_frame, width=11, style='Monitor.TLabel')
            energy_label.grid(row=1, column=1, sticky='nsew', padx=1, pady=0)
            
            # Separator
            separator_label = ttk.Label(stats_frame, text=" | ", style='Monitor.TLabel')
            separator_label.grid(row=1, column=2, sticky='nsew', padx=1, pady=0)
            
            # Second row: All auto states
            auto_shoot_label = ttk.Label(stats_frame, width=15, style='Monitor.TLabel')
            auto_shoot_label.grid(row=1, column=3, sticky='nsew', padx=1, pady=0)
            
            auto_aim_label = ttk.Label(stats_frame, width=13, style='Monitor.TLabel')
            auto_aim_label.grid(row=1, column=4, sticky='nsew', padx=1, pady=0)
            
            auto_pickup_label = ttk.Label(stats_frame, width=16, style='Monitor.TLabel')
            auto_pickup_label.grid(row=1, column=5, sticky='nsew', padx=1, pady=0)
            
            auto_hp_regen_label = ttk.Label(stats_frame, width=14, style='Monitor.TLabel')
            auto_hp_regen_label.grid(row=1, column=6, sticky='nsew', padx=1, pady=0)
            
            auto_energy_regen_label = ttk.Label(stats_frame, width=17, style='Monitor.TLabel')
            auto_energy_regen_label.grid(row=1, column=7, sticky='nsew', padx=1, pady=0)
            
            # Configure columns to expand properly
            for i in range(8):
                stats_frame.grid_columnconfigure(i, weight=1)
            
            self.char_labels[f"Character{char_num}"] = {
                'name': name_label,
                'hp': hp_label,
                'energy': energy_label,
                'separator': separator_label,
                'auto_shoot': auto_shoot_label,
                'auto_aim': auto_aim_label,
                'auto_pick_up': auto_pickup_label,
                'auto_hp_regen': auto_hp_regen_label,
                'auto_energy_regen': auto_energy_regen_label
            }
        
        # Start updating values
        self.update_values()
        
    def update_values(self):
        config = configparser.ConfigParser()
        config_path = Path(__file__).parent / 'config.ini'
        config.read(config_path)
    
        for char_num in range(1, 6):
            section = f"Character{char_num}"
            if section in config:
                # Update character name
                name = config[section].get('name', f'Character {char_num}')
                self.char_labels[section]['name'].config(
                    text=f"{name}",
                    foreground='#4A9EFF')
                
                try:
                    # Update energy level with blinking
                    energy = int(config[section].get('energy_level', '0'))
                    if energy < 20:
                        blink_color = '#FF4444' if int(time.time() * 2) % 2 else '#1E1E1E'  # Blink every 0.5 seconds
                    else:
                        blink_color = '#00FF44'
                    self.char_labels[section]['energy'].config(
                        text=f"Energy: {energy:3d}",  # Fixed width number
                        foreground=blink_color)
                    
                    # Update HP level with blinking
                    hp = int(config[section].get('hp_level', '0'))
                    if hp < 20:
                        blink_color = '#FF4444' if int(time.time() * 2) % 2 else '#1E1E1E'  # Blink every 0.5 seconds
                    else:
                        blink_color = '#00FF44'
                    self.char_labels[section]['hp'].config(
                        text=f"HP: {hp:3d}",  # Fixed width number
                        foreground=blink_color)
                    
                    # Update auto states
                    auto_shoot = "ON" if int(config[section].get('auto_shoot_state', '0')) else "OFF"
                    self.char_labels[section]['auto_shoot'].config(
                        text=f"Auto Shoot: {auto_shoot}",
                        foreground='#00FF44' if auto_shoot == "ON" else '#FF4444')
                    
                    auto_pick_up = "ON" if int(config[section].get('auto_pick_up_state', '0')) else "OFF"
                    self.char_labels[section]['auto_pick_up'].config(
                        text=f"Auto Pick Up: {auto_pick_up}",
                        foreground='#00FF44' if auto_pick_up == "ON" else '#FF4444')
                    
                    auto_hp = "ON" if int(config[section].get('auto_hp_regen_state', '0')) else "OFF"
                    self.char_labels[section]['auto_hp_regen'].config(
                        text=f"HP Regen: {auto_hp}",
                        foreground='#00FF44' if auto_hp == "ON" else '#FF4444')
                    
                    auto_energy = "ON" if int(config[section].get('auto_energy_regen_state', '0')) else "OFF"
                    self.char_labels[section]['auto_energy_regen'].config(
                        text=f"Energy Regen: {auto_energy}",
                        foreground='#00FF44' if auto_energy == "ON" else '#FF4444')
                    
                    auto_aim = "ON" if int(config[section].get('auto_aim_state', '0')) else "OFF"
                    self.char_labels[section]['auto_aim'].config(
                        text=f"Auto Aim: {auto_aim}",
                        foreground='#00FF44' if auto_aim == "ON" else '#FF4444')
                except (ValueError, KeyError) as e:
                    print(f"Error updating values for {section}: {e}")
    
        # Schedule next update
        self.root.after(100, self.update_values)
        
    # Add these new methods for window dragging
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

def main():
    root = tk.Tk()
    
    # Optional: Remove window decorations for a cleaner look
    root.overrideredirect(True)  # Uncomment if you want to remove window title bar
    
    app = MonitorGUI(root)
    
    # Update the window to calculate proper sizes
    root.update()
    
    # Get the required size and set it as the window size
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
