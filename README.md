# Foxcam

[![release](https://img.shields.io/badge/release-v1.0-blue)](https://github.com/HZDavy/Foxcam/releases)
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/HZDavy/Foxcam/blob/main/LICENSE)
[![python](https://img.shields.io/badge/python-3.10+-yellow)](https://www.python.org/)
[![platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows/)

轻量级 Windows 桌面应用，实时控制 UVC 摄像头参数。
Lightweight Windows desktop application for controlling UVC camera parameters in real-time.

<p align="center">
  <img src="docs/logo.png" alt="Foxcam" width="400">
</p>

## 界面截图 / Screenshot

<p align="center">
  <img src="docs/screenshot.png" alt="Foxcam Screenshot" width="700">
</p>

## 功能特性 / Features

- **多摄像头支持** — 同时检测和控制多个 USB 摄像头
  **Multi-camera support** — Detect and control multiple USB cameras simultaneously
- **实时参数调节** — 亮度、对比度、饱和度、色相、伽马、白平衡、曝光、变焦、对焦等
  **Real-time parameter adjustment** — Brightness, contrast, saturation, hue, gamma, white balance, exposure, zoom, focus, and more
- **自动/手动切换** — 每个参数可独立切换自动或手动模式
  **Auto/Manual toggle** — Switch between automatic and manual mode for each parameter
- **预设** — 为每个摄像头保存和加载参数配置
  **Presets** — Save and load parameter configurations per camera
- **组合** — 同时对多个摄像头应用预设组合
  **Combos** — Apply preset combinations across multiple cameras at once
- **Tab 拖拽排序** — 拖动标签页排序，顺序自动记忆
  **Tab drag-and-drop** — Reorder camera tabs by dragging, order is remembered
- **导入/导出** — 在不同机器之间共享预设
  **Import/Export** — Share presets between machines
- **深色主题** — 基于 CustomTkinter 的简洁现代深色 UI
  **Dark theme** — Clean, modern dark UI built with CustomTkinter

## 快速开始 / Quick Start

### 下载（无需 Python）/ Download (No Python required)

从 [Releases](https://github.com/HZDavy/Foxcam/releases) 下载最新版本，解压后运行 `Foxcam.exe`。
Download the latest release from [Releases](https://github.com/HZDavy/Foxcam/releases), extract the zip, and run `Foxcam.exe`.

### 从源码运行 / Run from Source

```bash
git clone https://github.com/HZDavy/Foxcam.git
cd Foxcam
pip install -r requirements.txt
python app.py
```

### 构建 EXE / Build EXE

```bash
pip install pyinstaller
pyinstaller --onedir --windowed --name Foxcam --icon foxcam.ico --add-data "icon.png;." --add-data "foxcam_logo.png;." --add-data "foxcam.ico;." --hidden-import duvc_ctl --hidden-import dshow --hidden-import customtkinter --hidden-import PIL app.py
```

## 系统要求 / Requirements

- Windows 10/11
- Python 3.10+（从源码运行时需要 / for running from source）
- 支持 UVC DirectShow 属性的 USB 摄像头
  USB camera(s) that support UVC DirectShow properties

## 依赖项 / Dependencies

- [duvc-ctl](https://github.com/allanhanan/duvc-ctl) — DirectShow 视频处理控制的 Python 封装，用于读取和设置摄像头属性
  Python wrapper for DirectShow Video Processing Amp control
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — 现代风格的 tkinter 控件
  Modern-looking tkinter widgets
- [Pillow](https://python-pillow.org/) — 图像处理，用于 UI 资源
  Image processing for UI assets

## 相关项目 / Related Projects

- **[duvc-ctl](https://github.com/allanhanan/duvc-ctl)** — 本项目依赖的核心库，用于 DirectShow 摄像头控制
  The core library this project depends on for DirectShow camera control
- **[camrenamer](https://github.com/oe7set/camrenamer/)** — USB 摄像头改名工具，在 Windows 中重命名摄像头，适合同型号多摄像头区分
  A tool to rename USB cameras in Windows, useful when you have multiple cameras of the same model

## 许可证 / License

本项目基于 MIT 许可证开源，详情参见 [LICENSE](LICENSE)。
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
