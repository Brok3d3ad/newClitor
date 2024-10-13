import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tkinter import Tk
from gui.main_window import TestToggleApp

if __name__ == "__main__":
    root = Tk()
    app = TestToggleApp(root)
    root.mainloop()