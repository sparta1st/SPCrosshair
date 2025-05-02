#🎯 SPCrosshair – Auto Crosshair for All FPS Games

**SPCrosshair.exe** is a smart, persistent, customizable on-screen crosshair that automatically appears when you launch popular FPS games like CS2, Valorant, or Fortnite.
It runs silently in the background and starts automatically with Windows – no manual setup needed.

---

## 💡 What It Does

* 🧠 **Automatically detects games** and shows the crosshair only when needed
* 🔄 **Runs at startup** (hidden) – no clicks, no clutter
* 🎯 **Draws a clean crosshair** in the center of your screen
* 🧾 **Settings are saved** permanently – no need to reconfigure every time

---

## 🖥️ Features

| Feature          | Description                                   |
| ---------------- | --------------------------------------------- |
| 🎨 Length        | Adjustable via `F1`                           |
| ↕️ Gap           | Adjustable via `F2`                           |
| 📏 Thickness     | Adjustable via `F3`                           |
| 🌈 Color         | Selectable via `F4` (preset colors)           |
| 🌫️ Opacity      | Adjustable via `F5`                           |
| 🧰 Extended HUD  | Full overview of settings with `F7`           |
| 🔁 Dual Profiles | Switch between Primary and Secondary with `C` |
| ♻️ Reset 2nd     | Reset secondary crosshair via `F8`            |
| ❌ Exit App       | Press `F9` anytime                            |

All settings are controlled via your keyboard + mouse scroll – no mouse clicking needed.

---

## ✅ Supported Games

SPCrosshair automatically activates when any of the following processes are detected:

* Counter-Strike 2 (`cs2.exe`)
* Counter-Strike: Global Offensive (`csgo.exe`)
* Valorant (`valorant.exe`)
* Fortnite (`fortniteclient-win64-shipping.exe`)
* Apex Legends (`r5apex.exe`)
* Call of Duty: MW2 / Warzone (`cod.exe`, `mw2.exe`, `warzone.exe`)
* Overwatch (`overwatch.exe`)
* Dota 2 (`dota2.exe`)
* Half-Life 2 (`hl2.exe`)
* Rainbow Six Siege (`rainbowsix.exe`)
* Palworld (`palworld-win64-shipping.exe`)
* Roblox (`robloxplayerbeta.exe`)
* Battlefield 2042 (`bf2042.exe`)
* Farlight 84 (`farlight84.exe`)

> ℹ️ Detection is based on background process names. If you want support for more games, open an issue on GitHub!

---

## 📦 How to Use

### 🔽 Step 1: Download

Grab the compiled EXE file from the [Releases](https://github.com/yourname/SPCrosshair/releases) section.

### 🖱️ Step 2: Launch Once

Just double-click `SPCrosshair.exe`. It will:

* Add itself to your Windows startup folder
* Run silently in the background
* Monitor for supported games

### 🧠 Step 3: Auto-Start + Auto-Show

Once a supported game launches, the crosshair UI will become visible.

No additional interaction needed!

---

## 📁 Persistence

All your settings (for both PRIMARY and SECONDARY targets) are saved inside:

```
%APPDATA%\.crosshair_data\settings.cfg
```

You can manually delete this file to reset to default values.

---

## 🙌 Contributing

Found a bug or want to add more games? Open a pull request or GitHub issue!

---

## 📜 License

MIT – Free to use, modify and distribute.
