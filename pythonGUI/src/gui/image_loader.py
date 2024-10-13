from PIL import Image, ImageTk

def load_icon(root, icon_path):
    """Loads and sets the window icon."""
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon_photo)
    return icon_photo

def load_background_image(root, background_path):
    """Loads and returns the background image."""
    background_image = Image.open(background_path)
    background_photo = ImageTk.PhotoImage(background_image)
    return background_photo
