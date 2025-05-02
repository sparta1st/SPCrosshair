import tkinter as tk
import configparser
import os
import threading
from pathlib import Path
from pynput import keyboard, mouse
import psutil
import time
import sys
APPDATA_PATH = Path(os.getenv("APPDATA")) / ".crosshair_data"
CONFIG_FILE = APPDATA_PATH / "settings.cfg"

defaults = {
    "length": 10,
    "gap": 5,
    "thickness": 2,
    "color": "0,255,255",
    "opacity": 0.6
}

colors = [
    ("Cyan", "0,255,255"),
    ("Red", "255,0,0"),
    ("Green", "0,255,0"),
    ("Blue", "0,0,255"),
    ("Yellow", "255,255,0"),
    ("Magenta", "255,0,255")
]

target = "PRIMARY"
targets = {"PRIMARY": {}, "SECONDARY": {}}
color_index = 0
ui_open = False
extended_open = False
selected = [None]

def ensure_config():
    APPDATA_PATH.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        config = configparser.ConfigParser()
        config["PRIMARY"] = defaults
        config["SECONDARY"] = defaults
        with open(CONFIG_FILE, "w") as f:
            config.write(f)

def load_config():
    ensure_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    for section in ["PRIMARY", "SECONDARY"]:
        targets[section] = {
            "length": int(config.get(section, "length", fallback=defaults["length"])),
            "gap": int(config.get(section, "gap", fallback=defaults["gap"])),
            "thickness": int(config.get(section, "thickness", fallback=defaults["thickness"])),
            "color": config.get(section, "color", fallback=defaults["color"]),
            "opacity": float(config.get(section, "opacity", fallback=defaults["opacity"]))
        }

def save_config():
    config = configparser.ConfigParser()
    config["PRIMARY"] = {k: str(v) for k, v in targets["PRIMARY"].items()}
    config["SECONDARY"] = {k: str(v) for k, v in targets["SECONDARY"].items()}
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

def get_color_name(rgb):
    for name, code in colors:
        if code == rgb:
            return name
    return "Custom"

def draw_crosshair(canvas, vals):
    canvas.delete("all")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    cx, cy = screen_width // 2, screen_height // 2

    t, l, g = vals["thickness"], vals["length"], vals["gap"]
    r, g_, b = map(int, vals["color"].split(","))
    color = f"#{r:02x}{g_:02x}{b:02x}"

    # Sus
    canvas.create_rectangle(
        cx - t // 2, cy - g - l,
        cx + (t + 1) // 2, cy - g,
        fill=color, width=0
    )

    # Jos
    canvas.create_rectangle(
        cx - t // 2, cy + g,
        cx + (t + 1) // 2, cy + g + l,
        fill=color, width=0
    )

    # Stânga
    canvas.create_rectangle(
        cx - g - l, cy - t // 2,
        cx - g, cy + (t + 1) // 2,
        fill=color, width=0
    )

    # Dreapta
    canvas.create_rectangle(
        cx + g + 1, cy - t // 2,
        cx + g + l + 1, cy + (t + 1) // 2,
        fill=color, width=0
    )







def update_hud():
    vals = targets[target]
    color_name = get_color_name(vals["color"])
    fields = [
        ("LENGTH", vals["length"], "F1"),
        ("GAP", vals["gap"], "F2"),
        ("THICKNESS", vals["thickness"], "F3"),
        ("COLOR", color_name, "F4"),
        ("OPACITY", vals["opacity"], "F5"),
        ("EXIT SETTINGS", "", "F6"),
        ("EXTENDED HUD", "", "F7"),
        ("CREATE 2ND", "", "F8"),
        ("EXIT APP", "", "F9"),
        ("SWITCH TARGET", "", "C")
    ]
    for i, label in enumerate(hud_rows):
        label["name"].config(text=f"{fields[i][0]:<13}:")
        label["value"].config(text=str(fields[i][1]))
        label["key"].config(text=f"[{fields[i][2]}]")

def update_extended():
    vals1, vals2 = targets["PRIMARY"], targets["SECONDARY"]
    def format_vals(v):
        return f"LENGTH: {v['length']}, GAP: {v['gap']}, THICKNESS: {v['thickness']}, COLOR: {get_color_name(v['color'])}, OPACITY: {v['opacity']}"
    text = f"ACTIVE: {target}\n\nPRIMARY:\n{format_vals(vals1)}\n\nSECONDARY:\n{format_vals(vals2)}\n\n[F8] Reset 2nd\n[C] Switch\n[F6] Exit HUD\n[F9] Exit App"
    extended_label.config(text=text)

def toggle_ui():
    global ui_open
    if ui_open:
        hud_window.withdraw()
    else:
        hud_window.deiconify()
        update_hud()
    ui_open = not ui_open

def toggle_extended():
    global extended_open
    if extended_open:
        extended_window.withdraw()
    else:
        extended_window.deiconify()
        update_extended()
    extended_open = not extended_open

def switch_target():
    global target
    target = "SECONDARY" if target == "PRIMARY" else "PRIMARY"
    draw_crosshair(canvas, targets[target])
    if ui_open:
        update_hud()
    if extended_open:
        update_extended()

def reset_secondary():
    targets["SECONDARY"] = defaults.copy()
    save_config()
    if extended_open:
        update_extended()


def adjust_selected_value(step):
    s = selected[0]
    if s == "color":
        global color_index
        color_index = (color_index + step) % len(colors)
        targets[target]["color"] = colors[color_index][1]
    elif s == "opacity":
        val = targets[target]["opacity"]
        targets[target]["opacity"] = max(0.1, min(1.0, round(val + (0.05 * step), 2)))
    else:
        targets[target][s] = max(1, targets[target][s] + step)
    save_config()
    draw_crosshair(canvas, targets[target])
    if ui_open:
        update_hud()


def on_press(key):
    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()

        if key == Key.f1:
            selected[0] = "length"
        elif key == Key.f2:
            selected[0] = "gap"
        elif key == Key.f3:
            selected[0] = "thickness"
        elif key == Key.f4:
            selected[0] = "color"
        elif key == Key.f5:
            selected[0] = "opacity"
        elif key == Key.f6:
            root.after(0, toggle_ui)
        elif key == Key.f7:
            root.after(0, toggle_extended)
        elif key == Key.f8:
            root.after(0, reset_secondary)
        elif key == Key.f9:
            sys.exit(0)
        elif hasattr(key, 'char') and key.char == 'c':
            root.after(0, switch_target)

        # Aplica doar dacă UI e deschis
        if ui_open and selected[0]:
            if key == Key.shift_l:
                adjust_selected_value(-1)
            elif key == Key.ctrl_l:
                adjust_selected_value(1)

        if ui_open:
            root.after(0, update_hud)

    except Exception as e:
        print("Error in on_press:", e)


# Game detection
game_exes = [
    "csgo.exe", "cs2.exe", "valorant.exe", "fortniteclient-win64-shipping.exe",
    "r5apex.exe", "cod.exe", "mw2.exe", "warzone.exe", "overwatch.exe",
    "dota2.exe", "hl2.exe", "rainbowsix.exe", "palworld-win64-shipping.exe",
    "robloxplayerbeta.exe", "bf2042.exe", "farlight84.exe"
]

def is_game_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() in game_exes:
            return True
    return False

def auto_crosshair_toggle():
    shown = False
    while True:
        if is_game_running():
            if not shown:
                print("✅ Game detected!")
                root.after(0, root.deiconify)
                root.after(10, lambda: draw_crosshair(canvas, targets[target]))
                shown = True
        else:
            if shown:
                print("❌ Game not detected.")
                root.after(0, root.withdraw)
                shown = False
        time.sleep(2)

# Init
load_config()
save_config()

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "black")
root.attributes("-alpha", 1.0)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

hud_window = tk.Toplevel(root)
hud_window.overrideredirect(True)
hud_window.attributes("-topmost", True)
hud_window.wm_attributes("-alpha", 0.6)
hud_window.configure(bg="white")
hud_window.geometry(f"340x300+{root.winfo_screenwidth() - 360}+40")

main_frame = tk.Frame(hud_window, bg="white")
main_frame.pack(padx=10, pady=8)
instruction = tk.Label(main_frame, text="Use mouse scroll to select option", font=("Consolas", 10), fg="#FF0000", bg="white")
instruction.pack(pady=(0, 10), anchor="w")

hud_rows = []
for _ in range(10):
    frame = tk.Frame(main_frame, bg="white")
    frame.pack(anchor="w")
    row = {
        "name": tk.Label(frame, font=("Consolas", 11), bg="white", fg="black", width=15, anchor="w"),
        "value": tk.Label(frame, font=("Consolas", 11), bg="white", fg="black", width=10, anchor="w"),
        "key": tk.Label(frame, font=("Consolas", 11), bg="white", fg="#FF0000", width=10, anchor="w")
    }
    row["name"].pack(side="left")
    row["value"].pack(side="left")
    row["key"].pack(side="left")
    hud_rows.append(row)

hud_window.withdraw()

extended_window = tk.Toplevel(root)
extended_window.overrideredirect(True)
extended_window.attributes("-topmost", True)
extended_window.wm_attributes("-alpha", 0.6)
extended_window.configure(bg="white")
extended_window.geometry(f"340x330+{root.winfo_screenwidth() - 360}+360")
extended_label = tk.Label(extended_window, text="", font=("Consolas", 10), justify="left", fg="black", bg="white", anchor="nw")
extended_label.pack(padx=10, pady=10, fill="both", expand=True)
extended_window.withdraw()

# Threads
keyboard.Listener(on_press=on_press, suppresed=False).start()
threading.Thread(target=auto_crosshair_toggle, daemon=True).start()

# Start
root.withdraw()
root.mainloop()
