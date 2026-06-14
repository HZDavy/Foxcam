# Foxcam

[![release](https://img.shields.io/badge/release-v1.0-blue)](https://github.com/HZDavy/Foxcam/releases)
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/HZDavy/Foxcam/blob/main/LICENSE)
[![python](https://img.shields.io/badge/python-3.10+-yellow)](https://www.python.org/)
[![platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows/)

A lightweight Windows desktop application for controlling UVC (USB Video Class) camera parameters in real-time.

<p align="center">
  <img src="docs/logo.png" alt="Foxcam" width="400">
</p>

## Screenshot

<p align="center">
  <img src="docs/screenshot.png" alt="Foxcam Screenshot" width="700">
</p>

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

Download the latest release from [Releases](https://github.com/HZDavy/Foxcam/releases). Two language versions are available:

- **[Foxcam-v1.0.zip](https://github.com/HZDavy/Foxcam/releases/download/v1.0/Foxcam-v1.0.zip)** — 中文版 (Chinese)
- **[Foxcam-EN-v1.0.zip](https://github.com/HZDavy/Foxcam/releases/download/v1.0/Foxcam-EN-v1.0.zip)** — English version

Extract the zip and run `Foxcam.exe`.

### Run from Source

```bash
git clone https://github.com/HZDavy/Foxcam.git
cd Foxcam
pip install -r requirements.txt
python app.py
```

### Build EXE

```bash
pip install pyinstaller
pyinstaller --onedir --windowed --name Foxcam --icon foxcam.ico --add-data "icon.png;." --add-data "foxcam_logo.png;." --add-data "foxcam.ico;." --hidden-import duvc_ctl --hidden-import dshow --hidden-import customtkinter --hidden-import PIL app.py
```

## Languages

Currently supported: **中文 (Chinese)** and **English**

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

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
