# 🕒 FloatingClock - Always on Top

A lightweight, always-on-top digital clock built with Python and Tkinter. Designed to run smoothly across **Linux (optimized for Linux Mint Cinnamon)**, **Windows**, and **macOS** with a tiny resource footprint (~15–20 MB RAM).

It stays visible across workspaces, supports drag-to-move, dynamic hover transparency, customizable themes, font sizing, and full system tray control.

## ✨ Features 

- **Flexible Time Formats:** Toggle easily between 12-hour (with AM/PM) and 24-hour clock formats via the system tray.
- **Optional Seconds:** Turn seconds on or off on the fly.
- **Always on Top:** Stays pinned above windows and across all virtual workspaces.
- **Drag-to-Move:** Click and drag the clock anywhere on your screen; positions are saved automatically.
- **Dynamic Transparency:** Diminishes opacity when your mouse leaves the window, and becomes more visible on hover.
- **Themes & Font Sizes:** Switch between *Dark*, *Light*, and *Blue* themes, or adjust font sizes dynamically.
- **System Tray Integration:** Manage your clock seamlessly from the system tray menu.
- **Cross-Platform:** Native support for Linux, Windows, and macOS.

## 📦 Requirements 

- Python 3.8+
- Dependencies: `pystray`, `Pillow`

### Installing Dependencies:
* **Linux (Mint/Ubuntu/Debian):**
  ```bash
  sudo apt install python3-tk python3-pil python3-pystray

```

* **Windows / macOS:**
```bash
pip install pystray Pillow

```



## 🚀 Run the App

Run interactively in a terminal:

```bash
python3 always_on_top_clock.py

```

Run in the background (survives terminal closure, e.g., on Linux):

```bash
nohup python3 /path/to/your/always_on_top_clock.py > /dev/null 2>&1 &
nohup python3 /home/panaivizhi/dev/always_on_top_clock/FloatingClock.py > /dev/null 2>&1 &
```

## 🖼️ Custom Tray Icon

The app automatically detects your OS and loads the correct icon format from the project root:

* **Windows:** Looks for `clock.ico`
* **Linux / macOS:** Looks for transparent `clock.png` (recommended 128x128 pixels)

## 📁 File Structure

```
floating-clock/
├── always_on_top_clock.py
├── clock.png           # (or clock.ico for Windows)
├── clock_config.json   # Auto-generated user preferences
├── README.md
└── .gitignore

```

## 📃 License

MIT License — free to use, modify, and distribute.

---

## 🤖 AI Assistance Disclosure

> This project was developed with the assistance of **AI collaboration**, which helped generate and refine the cross-platform code, optimize system tray support, and manage Linux environment configurations.
