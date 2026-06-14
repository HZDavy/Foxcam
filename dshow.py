import subprocess
import os
import json
import threading

_SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'camera_settings.json')
_EXE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dshow_setfreq.exe')
_lock = threading.Lock()


def _load_settings():
    try:
        with open(_SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _save_settings(data):
    with open(_SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_power_line_frequency(frequency_value):
    with _lock:
        if not os.path.exists(_EXE_PATH):
            return False
        try:
            result = subprocess.run(
                [_EXE_PATH, str(frequency_value)],
                capture_output=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return result.returncode == 0
        except Exception:
            return False


def get_power_line_frequency():
    data = _load_settings()
    return data.get('_power_line_frequency', 2)


def save_power_line_frequency(value):
    data = _load_settings()
    data['_power_line_frequency'] = value
    _save_settings(data)
