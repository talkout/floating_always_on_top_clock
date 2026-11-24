import tkinter as tk
import time
import pystray
from PIL import Image, ImageDraw
import threading
import json
import os
import sys
import platform

# ------------------ Config Handling ------------------

CONFIG_FILE = 'clock_config.json'

DEFAULT_CONFIG = {
    'x': None,
    'y': None,
    'font_size': 20,
    'theme': 'Dark',
    'show_seconds': False,
    'use_24hr': False  # <--- Added 24-hour preference default
}

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return {**DEFAULT_CONFIG, **data}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Failed to load config — {e}")
    return DEFAULT_CONFIG.copy()

def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

config = load_config()

# ------------------ Tkinter Setup ------------------

root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)

# ------------------ Theme Setup ------------------

THEMES = {
    'Dark': {'fg': 'white', 'bg': 'black'},
    'Light': {'fg': 'black', 'bg': 'white'},
    'Blue': {'fg': 'white', 'bg': '#003366'}
}

def apply_theme(name):
    config['theme'] = name
    theme = THEMES[name]
    label.config(fg=theme['fg'], bg=theme['bg'])
    root.configure(bg=theme['bg'])
    save_config()

# ------------------ Font Setup ------------------

DEFAULT_FONT = 'Consolas' if platform.system() in ['Windows', 'Darwin'] else 'Monospace'

def set_font(size):
    config['font_size'] = size
    label.config(font=(DEFAULT_FONT, size, 'bold'))
    save_config()

# ------------------ Clock Label ------------------

label = tk.Label(root, font=(DEFAULT_FONT, config['font_size'], 'bold'),
                 fg=THEMES[config['theme']]['fg'],
                 bg=THEMES[config['theme']]['bg'])
label.pack()

def update_clock():
    if label.winfo_exists():
        # Determine format dynamically based on config settings
        if config['use_24hr']:
            fmt = '%H:%M:%S' if config['show_seconds'] else '%H:%M'
        else:
            fmt = '%I:%M:%S %p' if config['show_seconds'] else '%I:%M %p'
            
        label.config(text=time.strftime(fmt))
        root.after(1000, update_clock)

update_clock()

# ------------------ Positioning ------------------

def load_position():
    root.update_idletasks()
    if config['x'] is not None and config['y'] is not None:
        root.geometry(f'+{config["x"]}+{config["y"]}')
    else:
        root.geometry('+0+0') # Top-left corner

load_position()

# ------------------ Drag-to-Move ------------------

def start_move(event):
    root._drag_start_x = event.x
    root._drag_start_y = event.y

def do_move(event):
    x = root.winfo_pointerx() - root._drag_start_x
    y = root.winfo_pointery() - root._drag_start_y
    root.geometry(f'+{x}+{y}')
    config['x'], config['y'] = x, y
    save_config()

for widget in (root, label):
    widget.bind("<ButtonPress-1>", start_move)
    widget.bind("<B1-Motion>", do_move)

# ------------------ Transparency (Cross-Platform) ------------------

def set_opacity(level):
    root.attributes('-alpha', level)

def on_enter(event): set_opacity(0.6)  # Hover opacity (~60%)
def on_leave(event): set_opacity(0.3)  # Idle opacity (~30%)

root.bind("<Enter>", on_enter)
root.bind("<Leave>", on_leave)
set_opacity(0.3)

# ------------------ Tray Icon Setup ------------------

def get_tray_icon():
    base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    icon_filename = 'clock.ico' if platform.system() == 'Windows' else 'clock.png'
    icon_path = os.path.join(base_path, icon_filename)
    
    try:
        return Image.open(icon_path)
    except Exception:
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((16, 20), '🕒', fill='white')
        return image

def create_icon():
    image = get_tray_icon()

    def on_show(icon, item): root.deiconify()
    def on_hide(icon, item): root.withdraw()
    def on_exit(icon, item):
        icon.stop()
        try:
            root.after_cancel(update_clock)
        except:
            pass
        root.destroy()

    def toggle_seconds(icon, item):
        config['show_seconds'] = not config['show_seconds']
        save_config()

    # <--- Added toggle function for 12/24 hour format
    def toggle_format(icon, item):
        config['use_24hr'] = not config['use_24hr']
        save_config()

    menu = pystray.Menu(
        pystray.MenuItem('Show Clock', on_show),
        pystray.MenuItem('Hide Clock', on_hide),
        pystray.MenuItem('Font: Small', lambda i, _: set_font(16)),
        pystray.MenuItem('Font: Large', lambda i, _: set_font(24)),
        pystray.MenuItem('Theme: Dark', lambda i, _: apply_theme('Dark')),
        pystray.MenuItem('Theme: Light', lambda i, _: apply_theme('Light')),
        pystray.MenuItem('Theme: Blue', lambda i, _: apply_theme('Blue')),
        pystray.MenuItem('Toggle Seconds', toggle_seconds),
        pystray.MenuItem('24-Hour Format', toggle_format, checked=lambda item: config['use_24hr']), # <--- Dynamic checkmark option
        pystray.MenuItem('Exit', on_exit)
    )

    tray_icon = pystray.Icon("floating_clock", image, "FloatingClock", menu)
    tray_icon.run()

threading.Thread(target=create_icon, daemon=True).start()

# ------------------ Main Loop ------------------

try:
    root.mainloop()
except KeyboardInterrupt:
    pass
