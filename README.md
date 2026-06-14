# Foxcam

A lightweight Windows desktop application for controlling UVC (USB Video Class) camera parameters in real-time.

![Foxcam](icon.png)

## Features

- **Multi-camera support** — Detect and control multiple USB cameras simultaneously
- **Real-time parameter adjustment** — Brightness, contrast, saturation, hue, gamma, white balance, exposure, zoom, focus, and more
- **Auto/Manual toggle** — Switch between automatic and manual mode for each parameter
- **Presets** — Save and load parameter configurations per camera
- **Combos** — Apply preset combinations across multiple cameras at once
- **Tab drag-and-drop** — Reorder camera tabs by dragging, order is remembered
- **Import/Export** — Share presets between machines
- **Dark theme** — Clean, modern dark UI built with CustomTkinter

## Quick Start

### Download (No Python required)

Download the latest release from [Releases](https://github.com/your-username/foxcam/releases), extract the zip, and run `Foxcam.exe`.

### Run from Source

```bash
git clone https://github.com/your-username/foxcam.git
cd foxcam
pip install -r requirements.txt
python app.py
```

### Build EXE

```bash
pip install pyinstaller
pyinstaller --onedir --windowed --name Foxcam --icon foxcam.ico --add-data "icon.png;." --add-data "foxcam_logo.png;." --add-data "foxcam.ico;." --hidden-import duvc_ctl --hidden-import dshow --hidden-import customtkinter --hidden-import PIL app.py
```

## Requirements

- Windows 10/11
- Python 3.10+ (for running from source)
- USB camera(s) that support UVC DirectShow properties

## Dependencies

- [duvc-ctl](https://github.com/allanhanan/duvc-ctl) — Python wrapper for DirectShow Video Processing Amp control, used to read and set camera properties
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern-looking tkinter widgets
- [Pillow](https://python-pillow.org/) — Image processing for UI assets

## Related Projects

- **[duvc-ctl](https://github.com/allanhanan/duvc-ctl)** — The core library this project depends on for DirectShow camera control
- **[camrenamer](https://github.com/oe7set/camrenamer/)** — A tool to rename USB cameras in Windows, useful when you have multiple cameras of the same model and need to tell them apart

## License

MIT
