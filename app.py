import sys
import os
import json
import gc
import ctypes
import threading
import customtkinter as ctk
import tkinter as tk
from PIL import Image

def _base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def _resource_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, _resource_path())
import warnings
warnings.filterwarnings('ignore')
import duvc_ctl as ctl
import dshow

SETTINGS_FILE = os.path.join(_base_path(), 'camera_settings.json')

ctk.set_appearance_mode('dark')

_GRAY_THEME = {
    "CTk": {"fg_color": ["#222222", "#222222"]},
    "CTkToplevel": {"fg_color": ["#222222", "#222222"]},
    "CTkFrame": {
        "corner_radius": 8, "border_width": 0,
        "fg_color": ["#222222", "#222222"],
        "top_fg_color": ["#2a2a2a", "#2a2a2a"],
        "border_color": ["#333333", "#333333"],
    },
    "CTkButton": {
        "corner_radius": 6, "border_width": 0,
        "fg_color": ["#6b6b7b", "#6b6b7b"],
        "hover_color": ["#5a5a6a", "#5a5a6a"],
        "border_color": ["#6b6b7b", "#6b6b7b"],
        "text_color": ["#ffffff", "#ffffff"],
        "text_color_disabled": ["#777777", "#777777"],
    },
    "CTkLabel": {
        "corner_radius": 0, "fg_color": "transparent",
        "text_color": ["#cccccc", "#cccccc"],
    },
    "CTkEntry": {
        "corner_radius": 6, "border_width": 1,
        "fg_color": ["#353535", "#353535"],
        "border_color": ["#555555", "#555555"],
        "text_color": ["#cccccc", "#cccccc"],
        "placeholder_text_color": ["#777777", "#777777"],
    },
    "CTkCheckBox": {
        "corner_radius": 4, "border_width": 2,
        "fg_color": ["#6b6b7b", "#6b6b7b"],
        "border_color": ["#888888", "#888888"],
        "hover_color": ["#5a5a6a", "#5a5a6a"],
        "checkmark_color": ["#ffffff", "#ffffff"],
        "text_color": ["#cccccc", "#cccccc"],
        "text_color_disabled": ["#777777", "#777777"],
    },
    "CTkSlider": {
        "corner_radius": 6, "button_corner_radius": 10,
        "border_width": 2, "button_length": 16,
        "fg_color": ["#444444", "#444444"],
        "progress_color": ["#888888", "#888888"],
        "button_color": ["#aaaaaa", "#aaaaaa"],
        "button_hover_color": ["#999999", "#999999"],
    },
    "CTkComboBox": {
        "corner_radius": 6, "border_width": 1,
        "fg_color": ["#353535", "#353535"],
        "border_color": ["#555555", "#555555"],
        "button_color": ["#6b6b7b", "#6b6b7b"],
        "button_hover_color": ["#5a5a6a", "#5a5a6a"],
        "text_color": ["#cccccc", "#cccccc"],
        "text_color_disabled": ["#777777", "#777777"],
    },
    "CTkOptionMenu": {
        "corner_radius": 6,
        "fg_color": ["#6b6b7b", "#6b6b7b"],
        "button_color": ["#5a5a6a", "#5a5a6a"],
        "button_hover_color": ["#555555", "#555555"],
        "text_color": ["#ffffff", "#ffffff"],
        "text_color_disabled": ["#777777", "#777777"],
    },
    "CTkScrollbar": {
        "corner_radius": 6, "border_spacing": 4,
        "fg_color": ["#222222", "#222222"],
        "button_color": ["#555555", "#555555"],
        "button_hover_color": ["#666666", "#666666"],
    },
    "CTkSwitch": {
        "corner_radius": 10, "border_width": 2, "button_length": 16,
        "fg_color": ["#444444", "#444444"],
        "progress_color": ["#888888", "#888888"],
        "button_color": ["#aaaaaa", "#aaaaaa"],
        "button_hover_color": ["#999999", "#999999"],
        "text_color": ["#cccccc", "#cccccc"],
        "text_color_disabled": ["#777777", "#777777"],
    },
    "CTkRadioButton": {
        "corner_radius": 10, "border_width_checked": 2, "border_width_unchecked": 2,
        "fg_color": ["#6b6b7b", "#6b6b7b"],
        "border_color": ["#888888", "#888888"],
        "hover_color": ["#5a5a6a", "#5a5a6a"],
        "text_color": ["#cccccc", "#cccccc"],
        "text_color_disabled": ["#777777", "#777777"],
    },
    "CTkProgressBar": {
        "corner_radius": 6, "border_width": 0,
        "fg_color": ["#444444", "#444444"],
        "progress_color": ["#888888", "#888888"],
        "border_color": ["#555555", "#555555"],
    },
    "CTkSegmentedButton": {
        "corner_radius": 6, "border_width": 0,
        "fg_color": ["#333333", "#333333"],
        "selected_color": ["#5a5a6a", "#5a5a6a"],
        "selected_hover_color": ["#5a5a6a", "#5a5a6a"],
        "unselected_color": ["#2a2a2a", "#2a2a2a"],
        "unselected_hover_color": ["#444444", "#444444"],
        "text_color": ["#cccccc", "#cccccc"],
        "text_color_disabled": ["#777777", "#777777"],
    },
    "CTkTextbox": {
        "corner_radius": 6, "border_width": 0,
        "fg_color": ["#353535", "#353535"],
        "border_color": ["#555555", "#555555"],
        "text_color": ["#cccccc", "#cccccc"],
        "scrollbar_button_color": ["#555555", "#555555"],
        "scrollbar_button_hover_color": ["#666666", "#666666"],
    },
    "CTkScrollableFrame": {
        "label_fg_color": "transparent",
    },
    "DropdownMenu": {
        "fg_color": ["#353535", "#353535"],
        "hover_color": ["#454545", "#454545"],
        "text_color": ["#cccccc", "#cccccc"],
    },
    "CTkFont": {
        "family": "Microsoft YaHei UI",
        "size": 13,
        "weight": "normal",
    },
}

_theme_file = os.path.join(_resource_path(), 'gray_theme.json')
import json as _json
with open(_theme_file, 'w') as _f:
    _json.dump(_GRAY_THEME, _f)
ctk.set_default_color_theme(_theme_file)

VP = ctl.VidProp
CP = ctl.CamProp
TO_STR = ctl.to_string

ALL_PROPS = [
    ('brightness', VP.Brightness, '亮度', (0, 255, 128), '☀', '#444444', '#dddddd'),
    ('contrast', VP.Contrast, '对比度', (0, 255, 128), '◐', '#444444', '#dddddd'),
    ('saturation', VP.Saturation, '饱和度', (0, 255, 128), '🎨', '#999999', '#c0392b'),
    ('hue', VP.Hue, '色相', (-180, 180, 0), '🌈', '#6699ff', '#ff6699'),
    ('sharpness', VP.Sharpness, '锐度', (0, 255, 128), '🔍', None, None),
    ('gamma', VP.Gamma, '伽马', (72, 500, 100), '🔘', None, None),
    ('white_balance', VP.WhiteBalance, '白平衡', (2000, 6500, 4600), '🌡', '#7799cc', '#ddb844'),
    ('video_backlight_compensation', VP.BacklightCompensation, '背光补偿', (0, 1, 0), '💡', '#444444', '#dddddd'),
    ('gain', VP.Gain, '增益', (0, 255, 0), '📶', '#444444', '#dddddd'),
    ('exposure', CP.Exposure, '曝光', (-13, -1, -6), '📷', '#444444', '#dddddd'),
    ('focus', CP.Focus, '对焦', (0, 250, 0), '🎯', None, None),
    ('zoom', CP.Zoom, '变焦', (100, 500, 100), '🔎', None, None),
    ('pan', CP.Pan, '水平移动', (-10, 10, 0), '↔', None, None),
    ('tilt', CP.Tilt, '垂直移动', (-10, 10, 0), '↕', None, None),
]
_PROP_ENUM_MAP = {k: pe for k, pe, _, _, _, _, _ in ALL_PROPS}

BLUE = '#6b6b7b'
GRAY = '#5a5a6a'


def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_cam_props(dev_index):
    result = ctl.open_camera(device_index=dev_index)
    if not result.is_ok():
        return None, result.error().description()
    cam = result.value()
    props = []
    for pk, pe, label, (fmin, fmax, fdef), icon, gc1, gc2 in ALL_PROPS:
        r = cam.get(pe)
        if not r.is_ok():
            continue
        rr = cam.get_range(pe)
        s = r.value()
        rng = rr.value() if rr.is_ok() else None
        if rng is None:
            continue
        val = s.value
        if val == 0 and fdef != 0:
            val = fdef
        props.append({
            'key': pk, 'label': label, 'icon': icon, 'value': val,
            'auto': TO_STR(s.mode) == 'AUTO',
            'min': rng.min, 'max': rng.max, 'default': fdef,
            'grad_c1': gc1, 'grad_c2': gc2,
        })
    cam = None
    gc.collect()
    return props, None


def set_cam_prop(dev_index, prop_key, value, is_auto):
    result = ctl.open_camera(device_index=dev_index)
    if not result.is_ok():
        return
    cam = result.value()
    pe = _PROP_ENUM_MAP.get(prop_key)
    if pe:
        if is_auto:
            cam.set_auto(pe)
        else:
            cam.set(pe, ctl.PropSetting(int(value), ctl.CamMode.Manual))
    cam = None
    gc.collect()


def next_name(existing, prefix):
    nums = []
    for n in existing:
        if n.startswith(prefix):
            rest = n[len(prefix):]
            if rest.isdigit():
                nums.append(int(rest))
    i = 1
    while i in nums:
        i += 1
    return f'{prefix}{i}'


class CenteredInputDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, text):
        super().__init__(parent)
        self.title(title)
        self.configure(fg_color='#222222')
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.result = None
        try:
            self.attributes('-toolwindow', True)
        except Exception:
            pass

        w, h = 320, 160
        self.update_idletasks()
        px = parent.winfo_x() + parent.winfo_width() // 2 - w // 2
        py = parent.winfo_y() + parent.winfo_height() // 2 - h // 2
        self.geometry(f'{w}x{h}+{px}+{py}')

        ctk.CTkLabel(self, text=text, font=ctk.CTkFont(size=12),
                     text_color='#cccccc').pack(anchor='w', padx=16, pady=(16, 4))
        self.entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.entry_var, width=280)
        self.entry.pack(padx=16, pady=(0, 12))
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda e: self._ok())

        btn_frame = ctk.CTkFrame(self, fg_color='transparent')
        btn_frame.pack(pady=(0, 12))
        ctk.CTkButton(btn_frame, text='确定', width=80, command=self._ok,
                      fg_color=BLUE, hover_color='#5a5a6a').pack(side='left', padx=4)
        ctk.CTkButton(btn_frame, text='取消', width=80, command=self._cancel,
                      fg_color=GRAY, hover_color='#4a4a5a').pack(side='left', padx=4)

    def _ok(self):
        self.result = self.entry_var.get()
        self.grab_release()
        self.destroy()

    def _cancel(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.wait_window()
        return self.result


class GradientSlider(ctk.CTkFrame):
    def __init__(self, parent, pmin, pmax, value, c1, c2, command, height=24, **kw):
        self._grad_img = None
        self.canvas = None
        self.pmin = pmin
        self.pmax = max(pmin + 1, pmax)
        self.val = value
        self.c1, self.c2 = c1, c2
        self.command = command
        self._lock = False
        super().__init__(parent, fg_color='transparent', height=height, **kw)

        self.canvas = tk.Canvas(self, height=height, highlightthickness=0, bg='#353535', bd=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', self._on_configure)
        self.canvas.bind('<ButtonPress-1>', self._press)
        self.canvas.bind('<B1-Motion>', self._drag)
        self.canvas.bind('<ButtonRelease-1>', self._release)

    def _lerp(self, c1, c2, t):
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _on_configure(self, e):
        w = e.width
        h = e.height
        img = tk.PhotoImage(width=w, height=h)
        for x in range(w):
            t = x / max(1, w - 1)
            color = self._lerp(self.c1, self.c2, t)
            img.put(color, to=(x, 0, x + 1, h))
        self._grad_img = img
        self._draw(w, h)

    def _draw(self, w=None, h=None, **kw):
        if not self.canvas:
            return
        self.canvas.delete('all')
        w = w or self.canvas.winfo_width()
        h = h or self.canvas.winfo_height()
        if self._grad_img:
            self.canvas.create_image(0, 0, anchor='nw', image=self._grad_img)
        ratio = (self.val - self.pmin) / (self.pmax - self.pmin)
        thumb_x = int(ratio * (w - h))
        cx = thumb_x + h // 2
        cy = h // 2
        tr = max(4, h // 2 - 3)
        self.canvas.create_oval(cx - tr - 1, cy - tr - 1, cx + tr + 1, cy + tr + 1,
                                fill='#3a3a3a', outline='')
        self.canvas.create_oval(cx - tr, cy - tr, cx + tr, cy + tr,
                                fill='#ffffff', outline='#888888', width=1.5)

    def _press(self, e):
        self._update(e.x)

    def _drag(self, e):
        self._update(e.x)

    def _release(self, e):
        pass

    def _update(self, x):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        ratio = max(0, min(1, (x - h // 2) / max(1, w - h)))
        new_val = int(self.pmin + ratio * (self.pmax - self.pmin))
        if new_val != self.val:
            self.val = new_val
            self._draw()
            if not self._lock and self.command:
                self.command(new_val)

    def set(self, value):
        self.val = max(self.pmin, min(self.pmax, int(value)))
        self._draw()

    def get(self):
        return self.val


class PropRow(ctk.CTkFrame):
    def __init__(self, parent, prop, dev_index):
        super().__init__(parent, fg_color='transparent')
        self.dev_index = dev_index
        self.key = prop['key']
        self.pmin, self.pmax = prop['min'], prop['max']
        self.default = prop['default']
        self._lock = False
        self._unsupported = (self.pmin == self.pmax)
        icon = prop.get('icon', '')

        if self._unsupported:
            ctk.CTkLabel(self, text=f'{icon} {prop["label"]}', width=100, anchor='w',
                         font=ctk.CTkFont(size=13), text_color='#666666').grid(
                             row=0, column=0, sticky='w', padx=(0, 4))
            ctk.CTkLabel(self, text='— 不支持', font=ctk.CTkFont(size=12),
                         text_color='#555555').grid(row=0, column=1, sticky='w', padx=8)
            self.columnconfigure(1, weight=1)
            return

        ctk.CTkLabel(self, text=f'{icon} {prop["label"]}', width=100, anchor='w',
                     font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky='w', padx=(0, 4))

        grad_c1 = prop.get('grad_c1')
        grad_c2 = prop.get('grad_c2')
        if grad_c1 and grad_c2:
            self.slider = GradientSlider(self, self.pmin, self.pmax, prop['value'],
                                         grad_c1, grad_c2, self._on_slider)
        else:
            self.slider = GradientSlider(self, self.pmin, self.pmax, prop['value'],
                                         '#888888', '#b0b0b0', self._on_slider)
        self.slider.grid(row=0, column=1, sticky='ew', padx=4)

        self.var = tk.StringVar(value=str(prop['value']))
        self.entry = ctk.CTkEntry(self, textvariable=self.var, width=60,
                                  justify='center', font=ctk.CTkFont(size=12, family='Consolas'))
        self.entry.grid(row=0, column=2, padx=4)
        self.entry.bind('<Return>', self._on_entry)
        self.entry.bind('<FocusOut>', self._on_entry)

        self.auto_var = ctk.BooleanVar(value=prop['auto'])
        ctk.CTkCheckBox(self, text='自动', variable=self.auto_var,
                        command=self._on_auto, font=ctk.CTkFont(size=11),
                        checkbox_width=18, checkbox_height=18).grid(row=0, column=3, padx=(4, 0))

        self.columnconfigure(1, weight=1)

    def _on_slider(self, val):
        if self._lock:
            return
        v = int(val)
        self._lock = True
        self.var.set(str(v))
        self._lock = False
        if not self.auto_var.get():
            threading.Thread(target=set_cam_prop,
                             args=(self.dev_index, self.key, v, False),
                             daemon=True).start()

    def _on_entry(self, event=None):
        if self._lock:
            return
        try:
            v = max(self.pmin, min(self.pmax, int(self.var.get())))
        except ValueError:
            v = int(self.slider.get())
        self._lock = True
        self.var.set(str(v))
        self.slider.set(v)
        self._lock = False
        if not self.auto_var.get():
            threading.Thread(target=set_cam_prop,
                             args=(self.dev_index, self.key, v, False),
                             daemon=True).start()

    def _on_auto(self):
        threading.Thread(target=set_cam_prop,
                         args=(self.dev_index, self.key, 0, self.auto_var.get()),
                         daemon=True).start()

    def get_value(self):
        if self._unsupported:
            return None, False
        try:
            v = self.slider.get()
        except Exception:
            v = int(self.var.get())
        return int(v), self.auto_var.get()

    def set_value(self, value, auto):
        if self._unsupported:
            return
        self._lock = True
        self.var.set(str(value))
        try:
            self.slider.set(value)
        except Exception:
            pass
        self.auto_var.set(auto)
        self._lock = False


class CameraTab(ctk.CTkFrame):
    def __init__(self, parent, name, dev_index, props_data):
        super().__init__(parent, fg_color='transparent')
        self.name = name
        self.dev_index = dev_index
        self.rows = {}
        self._sb_timer = None
        self._build(props_data)
        self._setup_overlay_scrollbar()

    def _build(self, props_data):
        ctk.CTkLabel(self, text=self.name, font=ctk.CTkFont(size=15, weight='bold'),
                     anchor='w').pack(anchor='w', padx=4, pady=(4, 8))

        self._scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent',
                                                     scrollbar_button_color='#222222',
                                                     scrollbar_button_hover_color='#222222')
        self._scroll_frame.pack(fill='both', expand=True)
        self._scroll_frame._scrollbar.configure(width=0)

        grid = ctk.CTkFrame(self._scroll_frame, fg_color='transparent')
        grid.pack(fill='both', expand=True)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        for i, prop in enumerate(props_data):
            r, c = divmod(i, 2)
            row = PropRow(grid, prop, self.dev_index)
            row.grid(row=r, column=c, sticky='ew', padx=4, pady=(6, 16))
            self.rows[prop['key']] = row

    def _setup_overlay_scrollbar(self):
        top = self.winfo_toplevel()
        self._overlay_canvas = tk.Canvas(top, width=10, highlightthickness=0,
                                          bg='#222222')
        self._overlay_canvas.place_forget()
        self._overlay_sb_thumb = self._overlay_canvas.create_rectangle(
            0, 0, 10, 50, fill='#666666', outline='')
        self._overlay_sb_height = 100

        self._overlay_canvas.bind('<ButtonPress-1>', self._sb_press)
        self._overlay_canvas.bind('<B1-Motion>', self._sb_drag)
        self._overlay_canvas.bind('<Enter>', lambda e: self._cancel_hide())
        self._overlay_canvas.bind('<Leave>', lambda e: self._schedule_hide())

        self._scroll_frame._parent_canvas.configure(
            yscrollcommand=self._on_scroll
        )

        self._bind_mousewheel(self._scroll_frame)

    def _bind_mousewheel(self, widget):
        widget.bind('<MouseWheel>', self._on_mousewheel, add='+')
        widget.bind('<Button-4>', self._on_mousewheel, add='+')
        widget.bind('<Button-5>', self._on_mousewheel, add='+')
        for child in widget.winfo_children():
            self._bind_mousewheel(child)

    def _is_scrollable(self):
        try:
            first, last = self._scroll_frame._parent_canvas.yview()
            return float(first) > 0.0 or float(last) < 1.0
        except Exception:
            return False

    def _on_mousewheel(self, event):
        if self._is_scrollable():
            self._show_overlay_sb()
        return None

    def _on_scroll(self, first, last):
        try:
            first_f, last_f = float(first), float(last)
        except Exception:
            return
        if first_f <= 0.0 and last_f >= 1.0:
            return
        self._show_overlay_sb()
        top = self.winfo_toplevel()
        total_h = self.winfo_height()
        x = self.winfo_rootx() - top.winfo_rootx() + self.winfo_width() - 12
        y = self.winfo_rooty() - top.winfo_toplevel().winfo_rooty() if hasattr(top, 'winfo_toplevel') else self.winfo_rooty()
        y = self.winfo_rooty() - top.winfo_rooty()
        h = self.winfo_height()
        thumb_h = max(30, int(h * (last_f - first_f)))
        thumb_y = int(h * first_f)
        self._overlay_sb_height = h
        self._overlay_canvas.place(x=x, y=y, height=h)
        self._overlay_canvas.coords(self._overlay_sb_thumb,
                                     1, thumb_y, 9, thumb_y + thumb_h)

    def _show_overlay_sb(self):
        top = self.winfo_toplevel()
        x = self.winfo_rootx() - top.winfo_rootx() + self.winfo_width() - 12
        y = self.winfo_rooty() - top.winfo_rooty()
        h = self.winfo_height()
        self._overlay_canvas.place(x=x, y=y, height=h)
        self._overlay_canvas.tk.call('raise', self._overlay_canvas._w)
        self._cancel_hide()
        self._schedule_hide()

    def _cancel_hide(self):
        if self._sb_timer:
            self.after_cancel(self._sb_timer)
            self._sb_timer = None

    def _schedule_hide(self):
        self._cancel_hide()
        self._sb_timer = self.after(1500, self._hide_overlay_sb)

    def _hide_overlay_sb(self):
        self._overlay_canvas.place_forget()
        self._sb_timer = None

    def _sb_press(self, event):
        self._sb_drag_y = event.y
        self._sb_drag_start = self._scroll_frame._parent_canvas.yview()[0]

    def _sb_drag(self, event):
        dy = event.y - self._sb_drag_y
        total_h = self._overlay_sb_height
        if total_h <= 0:
            return
        fraction = dy / total_h
        self._scroll_frame._parent_canvas.yview_moveto(self._sb_drag_start + fraction)

    def get_settings(self):
        return {k: {'value': v, 'auto': a} for k, row in self.rows.items()
                for v, a in [row.get_value()]}

    def apply_settings(self, settings):
        for k, row in self.rows.items():
            if k in settings:
                s = settings[k]
                val = s['value'] if isinstance(s, dict) else int(s)
                auto = s.get('auto', False) if isinstance(s, dict) else False
                row.set_value(val, auto)
                threading.Thread(target=set_cam_prop,
                                 args=(self.dev_index, k, val, auto),
                                 daemon=True).start()

    def reload(self):
        def _do():
            props, _ = read_cam_props(self.dev_index)
            if props:
                self.after(0, lambda: [self.rows[p['key']].set_value(p['value'], p['auto'])
                                       for p in props if p['key'] in self.rows])
        threading.Thread(target=_do, daemon=True).start()

    def reset(self):
        for k, row in self.rows.items():
            row.set_value(row.default, False)
            threading.Thread(target=set_cam_prop,
                             args=(self.dev_index, k, row.default, False),
                             daemon=True).start()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Foxcam v1.1')
        self.geometry('1020x560')
        self.minsize(800, 420)
        self.configure(fg_color='#222222')
        self.withdraw()
        self.after(50, self._center_and_show)

    def _center_and_show(self):
        self._center_window()
        self.deiconify()

    def _center_window(self):
        self.update_idletasks()
        req_w = self.winfo_reqwidth()
        req_h = self.winfo_reqheight()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - req_w) // 2
        y = (sh - req_h) // 2
        self.geometry(f'+{x}+{y}')

        _icon_path = os.path.join(_resource_path(), 'foxcam.ico')
        if os.path.exists(_icon_path):
            self.after(100, lambda: self.iconbitmap(_icon_path))

        self._build_toolbar()
        ctk.CTkFrame(self, height=1, fg_color='#3a3a3a').pack(fill='x')

        self._build_combo_bar()

        self.notebook = ctk.CTkTabview(self, anchor='nw')
        self.notebook.pack(fill='both', expand=True, padx=8, pady=(4, 0))

        self._build_preset_bar()

        self.tabs = {}
        self._last_tab_name = ''
        self.after(200, self.scan)
        self.after(500, self._poll_tab_change)

    def _build_toolbar(self):
        tb = ctk.CTkFrame(self, fg_color='transparent')
        tb.pack(fill='x', padx=8, pady=6)

        _logo_path = os.path.join(_resource_path(), 'foxcam_logo.png')
        if os.path.exists(_logo_path):
            _logo_img = ctk.CTkImage(light_image=Image.open(_logo_path),
                                      dark_image=Image.open(_logo_path),
                                      size=(160, 36))
            ctk.CTkLabel(tb, image=_logo_img, text='').pack(side='left')
            self._logo_ref = _logo_img
        else:
            ctk.CTkLabel(tb, text='📷 Foxcam', font=ctk.CTkFont(size=16, weight='bold'),
                         text_color='#e0e0e0').pack(side='left')

        ctk.CTkButton(tb, text='🔍 扫描', width=70, command=self.scan,
                      fg_color=BLUE, hover_color='#5a5a6a').pack(side='left', padx=(16, 4))
        ctk.CTkButton(tb, text='🔄 重读', width=60, command=self._reload_current,
                      fg_color=BLUE, hover_color='#5a5a6a').pack(side='left', padx=4)
        ctk.CTkButton(tb, text='↺ 默认', width=60, command=self._reset_current,
                      fg_color=GRAY, hover_color='#444444').pack(side='left', padx=4)

        self._pinned = False
        self._pin_btn = ctk.CTkButton(tb, text='📌 置顶', width=60,
                                       command=self._toggle_pin,
                                       fg_color=GRAY, hover_color='#444444')
        self._pin_btn.pack(side='right', padx=4)

        self._freq_var = ctk.StringVar(value='50 Hz')
        saved_freq = dshow.get_power_line_frequency()
        if saved_freq == 3:
            self._freq_var.set('60 Hz')
        self._freq_cb = ctk.CTkComboBox(tb, values=['50 Hz', '60 Hz'],
                                         variable=self._freq_var, width=85,
                                         state='readonly', command=self._on_freq_change,
                                         fg_color='#353535', border_color='#555555',
                                         button_color=GRAY, button_hover_color='#444444',
                                         dropdown_fg_color='#353535',
                                         dropdown_hover_color='#454545')
        self._freq_cb.pack(side='right', padx=(2, 8))
        ctk.CTkLabel(tb, text='⚡ 防闪烁', font=ctk.CTkFont(size=11),
                     text_color='#999999').pack(side='right', padx=2)

    def _build_combo_bar(self):
        cf = ctk.CTkFrame(self, fg_color='#2a2a2a', corner_radius=6)
        cf.pack(fill='x', padx=8, pady=(0, 4))

        ctk.CTkLabel(cf, text='🔗 组合', font=ctk.CTkFont(size=12, weight='bold'),
                     text_color='#b0b0b0').pack(side='left', padx=(8, 4), pady=6)
        self.combo_var = ctk.StringVar()
        self.combo_cb = ctk.CTkComboBox(cf, values=[], variable=self.combo_var,
                                        width=160, state='readonly',
                                        fg_color='#353535', border_color='#555565',
                                        button_color=BLUE, button_hover_color='#5a5a6a',
                                        dropdown_fg_color='#353535',
                                        dropdown_hover_color='#454545')
        self.combo_cb.pack(side='left', padx=4, pady=6)
        ctk.CTkButton(cf, text='▶ 应用', width=50, command=self._combo_apply,
                      fg_color=BLUE, hover_color='#5a5a6a').pack(side='left', padx=2, pady=6)
        ctk.CTkButton(cf, text='💾 保存', width=50, command=self._combo_save,
                      fg_color=BLUE, hover_color='#5a5a6a').pack(side='left', padx=2, pady=6)
        self._combo_up_btn = self._make_arrow_btn(cf, '▲', lambda: self._combo_move(-1))
        self._combo_up_btn.pack(side='left', padx=(1, 0), pady=6)
        self._combo_dn_btn = self._make_arrow_btn(cf, '▼', lambda: self._combo_move(1))
        self._combo_dn_btn.pack(side='left', padx=0, pady=6)
        ctk.CTkButton(cf, text='🗑 删除', width=50, command=self._combo_del,
                      fg_color=GRAY, hover_color='#444444').pack(side='right', padx=2, pady=6)
        ctk.CTkButton(cf, text='✏ 重命名', width=60, command=self._combo_rename,
                      fg_color=GRAY, hover_color='#444444').pack(side='right', padx=2, pady=6)

    def _build_preset_bar(self):
        pf = ctk.CTkFrame(self, fg_color='#2a2a2a', corner_radius=6)
        pf.pack(fill='x', padx=8, pady=(4, 8))

        ctk.CTkLabel(pf, text='📋 预设', font=ctk.CTkFont(size=12, weight='bold'),
                     text_color='#b0b0b0').pack(side='left', padx=(8, 4), pady=6)
        self.preset_var = ctk.StringVar()
        self.preset_cb = ctk.CTkComboBox(pf, values=[], variable=self.preset_var,
                                         width=160, state='readonly',
                                         fg_color='#353535', border_color='#555565',
                                         button_color=BLUE, button_hover_color='#5a5a6a',
                                         dropdown_fg_color='#353535',
                                         dropdown_hover_color='#454545')
        self.preset_cb.pack(side='left', padx=4, pady=6)
        ctk.CTkButton(pf, text='▶ 应用', width=50, command=self._preset_apply,
                      fg_color=BLUE, hover_color='#5a5a6a').pack(side='left', padx=2, pady=6)
        ctk.CTkButton(pf, text='💾 保存', width=50, command=self._preset_save,
                      fg_color=BLUE, hover_color='#5a5a6a').pack(side='left', padx=2, pady=6)
        self._preset_up_btn = self._make_arrow_btn(pf, '▲', lambda: self._preset_move(-1))
        self._preset_up_btn.pack(side='left', padx=(1, 0), pady=6)
        self._preset_dn_btn = self._make_arrow_btn(pf, '▼', lambda: self._preset_move(1))
        self._preset_dn_btn.pack(side='left', padx=0, pady=6)
        ctk.CTkButton(pf, text='🗑 删除', width=50, command=self._preset_del,
                      fg_color=GRAY, hover_color='#444444').pack(side='right', padx=2, pady=6)
        ctk.CTkButton(pf, text='✏ 重命名', width=60, command=self._preset_rename,
                      fg_color=GRAY, hover_color='#444444').pack(side='right', padx=2, pady=6)
        ctk.CTkButton(pf, text='📤 导出', width=50, command=self._preset_export,
                      fg_color=GRAY, hover_color='#444444').pack(side='right', padx=2, pady=6)
        ctk.CTkButton(pf, text='📥 导入', width=50, command=self._preset_import,
                      fg_color=GRAY, hover_color='#444444').pack(side='right', padx=2, pady=6)

    def _make_arrow_btn(self, parent, text, command):
        btn = ctk.CTkButton(parent, text=text, width=18, height=22,
                            font=ctk.CTkFont(size=11), command=command,
                            fg_color='transparent', hover_color='#3a3a3a',
                            text_color='#555555', corner_radius=2)
        return btn

    def _combo_move(self, direction):
        name = self.combo_var.get()
        if not name:
            return
        data = self._data()
        combos = data.get('_combos', {})
        names = list(combos.keys())
        if name not in names:
            return
        idx = names.index(name)
        new_idx = idx + direction
        if new_idx < 0 or new_idx >= len(names):
            return
        names[idx], names[new_idx] = names[new_idx], names[idx]
        new_combos = {k: combos[k] for k in names}
        data['_combos'] = new_combos
        self._save_data(data)
        self._refresh_combos()
        self.combo_var.set(name)

    def _preset_move(self, direction):
        name = self.preset_var.get()
        if not name:
            return
        tab = self._current_tab()
        if not tab:
            return
        data = self._data()
        presets = data.get('_presets', {}).get(tab.name, {})
        names = list(presets.keys())
        if name not in names:
            return
        idx = names.index(name)
        new_idx = idx + direction
        if new_idx < 0 or new_idx >= len(names):
            return
        names[idx], names[new_idx] = names[new_idx], names[idx]
        new_presets = {k: presets[k] for k in names}
        data['_presets'][tab.name] = new_presets
        self._save_data(data)
        self._refresh_presets()
        self.preset_var.set(name)

    def _poll_tab_change(self):
        current = self.notebook.get()
        if current and current != self._last_tab_name:
            self._last_tab_name = current
            self._refresh_presets()
        self.after(200, self._poll_tab_change)

    def _current_tab(self):
        sel = self.notebook.get()
        if not sel:
            return None
        return self.tabs.get(sel)

    def _toggle_pin(self):
        self._pinned = not self._pinned
        self.attributes('-topmost', self._pinned)
        self._pin_btn.configure(text='📌 取消' if self._pinned else '📌 置顶',
                                fg_color='#8b0000' if self._pinned else GRAY)

    def _on_freq_change(self, value):
        freq_val = 2 if value == '50 Hz' else 3
        dshow.save_power_line_frequency(freq_val)
        threading.Thread(target=dshow.set_power_line_frequency,
                         args=(freq_val,), daemon=True).start()

    def _reload_current(self):
        tab = self._current_tab()
        if tab:
            tab.reload()

    def _reset_current(self):
        tab = self._current_tab()
        if tab:
            tab.reset()

    def scan(self):
        for tab_name in list(self.notebook._tab_dict.keys()):
            try:
                self.notebook.delete(tab_name)
            except Exception:
                pass
        self.tabs.clear()

        def _do():
            all_devs = list(ctl.list_devices())
            physical = [(i, d) for i, d in enumerate(all_devs)
                        if d.path.startswith('\\\\?\\usb#')]
            results = []
            for idx, d in physical:
                props, _ = read_cam_props(idx)
                results.append((idx, d.name, props or []))
            self.after(0, lambda: self._on_scan(results))

        threading.Thread(target=_do, daemon=True).start()

    def _on_scan(self, results):
        data = load_json(SETTINGS_FILE)
        saved_order = data.get('_tab_order', [])
        order_map = {name: i for i, name in enumerate(saved_order)}
        results.sort(key=lambda r: order_map.get(r[1], 999))

        for idx, name, props in results:
            if not props:
                props = [{'key': k, 'label': cn, 'icon': ic, 'value': d, 'auto': False,
                          'min': mn, 'max': mx, 'default': d,
                          'grad_c1': gc1, 'grad_c2': gc2}
                         for k, _, cn, (mn, mx, d), ic, gc1, gc2 in ALL_PROPS]
            frame = self.notebook.add(name)
            tab = CameraTab(frame, name, idx, props)
            tab.pack(fill='both', expand=True)
            self.tabs[name] = tab
        self._refresh_presets()
        self._refresh_combos()
        self._setup_tab_drag()

    def _setup_tab_drag(self):
        sb = self.notebook._segmented_button
        self._drag_data = {'name': None, 'start_x': 0}
        self._drag_indicator = None
        for name, btn in sb._buttons_dict.items():
            btn.bind('<ButtonPress-1>',
                     lambda e, n=name: self._tab_drag_start(e, n), add='+')
            btn.bind('<B1-Motion>',
                     lambda e, n=name: self._tab_drag_motion(e, n), add='+')
            btn.bind('<ButtonRelease-1>',
                     lambda e, n=name: self._tab_drag_end(e, n), add='+')

    def _tab_drag_start(self, event, name):
        self._drag_data = {'name': name, 'start_x': event.x_root}

    def _tab_drag_motion(self, event, name):
        if not self._drag_data['name']:
            return
        dx = event.x_root - self._drag_data['start_x']
        if abs(dx) < 10:
            return
        if not self._drag_indicator:
            self._drag_indicator = tk.Toplevel(self)
            self._drag_indicator.overrideredirect(True)
            self._drag_indicator.attributes('-topmost', True)
            self._drag_indicator.configure(bg='#4a9eff')
            lbl = tk.Label(self._drag_indicator, text=name,
                           bg='#4a9eff', fg='white',
                           font=ctk.CTkFont(size=12, weight='bold'))
            lbl.pack(padx=8, pady=4)
        self._drag_indicator.geometry(
            f'+{event.x_root - 40}+{event.y_root - 20}')

    def _tab_drag_end(self, event, name):
        if self._drag_indicator:
            self._drag_indicator.destroy()
            self._drag_indicator = None
        if not self._drag_data['name']:
            return
        dx = event.x_root - self._drag_data['start_x']
        if abs(dx) < 10:
            self._drag_data = {'name': None, 'start_x': 0}
            return
        sb = self.notebook._segmented_button
        names = list(sb._buttons_dict.keys())
        if name not in names:
            self._drag_data = {'name': None, 'start_x': 0}
            return
        btn = sb._buttons_dict[name]
        btn_x = btn.winfo_rootx() + btn.winfo_width() // 2
        drop_idx = len(names)
        for i, n in enumerate(names):
            if n == name:
                continue
            other_btn = sb._buttons_dict[n]
            other_x = other_btn.winfo_rootx() + other_btn.winfo_width() // 2
            if event.x_root < other_x:
                drop_idx = i
                break
        names.remove(name)
        src_idx = names.index(name) if name in names else len(names)
        if drop_idx > src_idx:
            drop_idx -= 1
        names.insert(min(drop_idx, len(names)), name)
        self._reorder_tabs(names)
        self._drag_data = {'name': None, 'start_x': 0}

    def _reorder_tabs(self, new_order):
        tab_contents = {}
        for name, tab in self.tabs.items():
            tab_contents[name] = {
                'dev_index': tab.dev_index,
                'settings': tab.get_settings(),
            }
        current = self.notebook.get()
        for tab_name in list(self.notebook._tab_dict.keys()):
            try:
                self.notebook.delete(tab_name)
            except Exception:
                pass
        self.tabs.clear()
        for name in new_order:
            if name not in tab_contents:
                continue
            info = tab_contents[name]
            props, _ = read_cam_props(info['dev_index'])
            if not props:
                props = [{'key': k, 'label': cn, 'icon': ic, 'value': d, 'auto': False,
                          'min': mn, 'max': mx, 'default': d,
                          'grad_c1': gc1, 'grad_c2': gc2}
                         for k, _, cn, (mn, mx, d), ic, gc1, gc2 in ALL_PROPS]
            frame = self.notebook.add(name)
            tab = CameraTab(frame, name, info['dev_index'], props)
            tab.pack(fill='both', expand=True)
            self.tabs[name] = tab
            if name in info['settings']:
                tab.apply_settings(info['settings'])
        if current in self.tabs:
            self.notebook.set(current)
        data = load_json(SETTINGS_FILE)
        data['_tab_order'] = new_order
        save_json(SETTINGS_FILE, data)
        self._setup_tab_drag()

    def _data(self):
        return load_json(SETTINGS_FILE)

    def _save_data(self, data):
        save_json(SETTINGS_FILE, data)

    def _refresh_presets(self):
        tab = self._current_tab()
        data = self._data()
        presets = list(data.get('_presets', {}).get(tab.name, {}).keys()) if tab else []
        self.combo_cb.configure(values=presets)
        self.preset_cb.configure(values=presets)
        self.preset_var.set('')
        self._refresh_combos()

    def _refresh_combos(self):
        data = self._data()
        combos = list(data.get('_combos', {}).keys())
        self.combo_cb.configure(values=combos)
        self.combo_var.set('')

    def _preset_save(self):
        tab = self._current_tab()
        if not tab:
            return
        data = self._data()
        presets = data.setdefault('_presets', {}).setdefault(tab.name, {})
        existing_names = list(presets.keys())
        name = CenteredInputDialog(self, '保存预设', '输入预设名称：').get_input()
        if name is None:
            return
        name = name.strip() or next_name(existing_names, '预设')
        presets[name] = tab.get_settings()
        self._save_data(data)
        self._refresh_presets()
        self.preset_var.set(name)

    def _preset_apply(self):
        tab = self._current_tab()
        if not tab:
            return
        name = self.preset_var.get()
        if not name:
            return
        data = self._data()
        settings = data.get('_presets', {}).get(tab.name, {}).get(name)
        if settings:
            tab.apply_settings(settings)

    def _preset_del(self):
        tab = self._current_tab()
        if not tab:
            return
        name = self.preset_var.get()
        if not name:
            return
        data = self._data()
        data.get('_presets', {}).get(tab.name, {}).pop(name, None)
        self._save_data(data)
        self._refresh_presets()

    def _preset_rename(self):
        tab = self._current_tab()
        if not tab:
            return
        old_name = self.preset_var.get()
        if not old_name:
            return
        new_name = CenteredInputDialog(self, '重命名预设', f'当前：{old_name}\n输入新名称：').get_input()
        if not new_name or new_name.strip() == old_name:
            return
        new_name = new_name.strip()
        data = self._data()
        presets = data.get('_presets', {}).get(tab.name, {})
        if new_name in presets:
            return
        presets[new_name] = presets.pop(old_name, {})
        self._save_data(data)
        self._refresh_presets()
        self.preset_var.set(new_name)

    def _preset_export(self):
        from tkinter import filedialog
        tab = self._current_tab()
        if not tab:
            return
        path = filedialog.asksaveasfilename(defaultextension='.json',
                                            filetypes=[('JSON', '*.json')])
        if not path:
            return
        data = self._data()
        save_json(path, {tab.name: data.get('_presets', {}).get(tab.name, {})})

    def _preset_import(self):
        from tkinter import filedialog
        tab = self._current_tab()
        if not tab:
            return
        path = filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
        if not path:
            return
        imported = load_json(path)
        data = self._data()
        presets = data.setdefault('_presets', {}).setdefault(tab.name, {})
        presets.update(imported.get(tab.name, {}))
        self._save_data(data)
        self._refresh_presets()

    def _combo_save(self):
        data = self._data()
        combos = data.setdefault('_combos', {})
        existing_names = list(combos.keys())

        dlg = ctk.CTkToplevel(self)
        dlg.title('保存组合')
        dlg.geometry('380x320')
        dlg.transient(self)
        dlg.grab_set()
        dlg.configure(fg_color='#222222')
        try:
            dlg.attributes('-toolwindow', True)
        except Exception:
            pass
        self.update_idletasks()
        x = self.winfo_x() + self.winfo_width() // 2 - 190
        y = self.winfo_y() + self.winfo_height() // 2 - 160
        dlg.geometry(f'380x320+{x}+{y}')

        ctk.CTkLabel(dlg, text='组合名称', font=ctk.CTkFont(size=12, weight='bold'),
                     text_color='#b0b0b0').pack(anchor='w', padx=12, pady=(12, 0))
        name_var = ctk.StringVar(value=next_name(existing_names, '组合'))
        ctk.CTkEntry(dlg, textvariable=name_var, width=300).pack(padx=12, pady=(4, 8))

        ctk.CTkLabel(dlg, text='为每个摄像头选择预设：',
                     font=ctk.CTkFont(size=11), text_color='#888888').pack(anchor='w', padx=12)

        cam_vars = {}
        for cam_name, tab in self.tabs.items():
            frame = ctk.CTkFrame(dlg, fg_color='#2a2a2a', corner_radius=4)
            frame.pack(fill='x', padx=12, pady=2)
            ctk.CTkLabel(frame, text=cam_name, width=180, anchor='w',
                         font=ctk.CTkFont(size=11)).pack(side='left', padx=4, pady=4)
            cam_presets = list(data.get('_presets', {}).get(cam_name, {}).keys())
            var = ctk.StringVar()
            cb = ctk.CTkComboBox(frame, values=cam_presets, variable=var,
                                 width=150, state='readonly',
                                 fg_color='#353535', border_color='#555565',
                                 button_color=BLUE, dropdown_fg_color='#353535')
            cb.pack(side='left', padx=4, pady=4)
            if cam_presets:
                cb.set(cam_presets[0])
            cam_vars[cam_name] = var

        def _ok():
            name = name_var.get().strip() or next_name(existing_names, '组合')
            mapping = {cn: v.get() for cn, v in cam_vars.items() if v.get()}
            if not mapping:
                return
            combos[name] = mapping
            self._save_data(data)
            self._refresh_combos()
            self.combo_var.set(name)
            dlg.destroy()

        ctk.CTkButton(dlg, text='✓ 确定', width=100, command=_ok,
                      fg_color=BLUE, hover_color='#5a5a6a').pack(pady=12)

    def _combo_apply(self):
        name = self.combo_var.get()
        if not name:
            return
        data = self._data()
        combo = data.get('_combos', {}).get(name)
        if not combo:
            return
        all_presets = data.get('_presets', {})
        for cam_name, preset_name in combo.items():
            tab = self.tabs.get(cam_name)
            settings = all_presets.get(cam_name, {}).get(preset_name)
            if tab and settings:
                tab.apply_settings(settings)

    def _combo_del(self):
        name = self.combo_var.get()
        if not name:
            return
        data = self._data()
        data.get('_combos', {}).pop(name, None)
        self._save_data(data)
        self._refresh_combos()

    def _combo_rename(self):
        old_name = self.combo_var.get()
        if not old_name:
            return
        new_name = CenteredInputDialog(self, '重命名组合', f'当前：{old_name}\n输入新名称：').get_input()
        if not new_name or new_name.strip() == old_name:
            return
        new_name = new_name.strip()
        data = self._data()
        combos = data.get('_combos', {})
        if new_name in combos:
            return
        combos[new_name] = combos.pop(old_name, {})
        self._save_data(data)
        self._refresh_combos()
        self.combo_var.set(new_name)


if __name__ == '__main__':
    app = App()
    app.mainloop()
