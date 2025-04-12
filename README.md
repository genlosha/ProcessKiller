# 🔒 Process Killer Hotkey Manager

A Python-based CLI tool that allows you to **assign global keyboard shortcuts to kill specific processes**. Useful for quickly terminating resource-heavy or buggy applications using custom hotkeys. For Windows users a built .exe-Version is available. 

---


## 🛠 Requirements to build

- Python 3.9+
- [`psutil`](https://pypi.org/project/psutil/)
- [`pynput`](https://pypi.org/project/pynput/)

Install dependencies:
```bash
pip install psutil pynput
```

---

## ▶️ Usage

Open **ProcessKiller.exe** or run the script:

```bash
python ProcessKiller.py
```

Then:
- Use the default shortcut `<Ctrl> + <Shift> + <Alt> + E` to open the shortcut editor.
- In the editor:
  - `assign` or `a`: Create a new shortcut to kill one or more processes.
  - `remove` or `r`: Delete an existing shortcut.
  - `continue` or `c`: Exit editor and re-enable shortcuts.
  - `exit` or `e`: Save & quit the program.

Shortcuts are saved to `stored_shortcuts.json`.


---

## ❗ Notes

- Hotkeys must follow `pynput` syntax (`<ctrl>+<alt>+d`, etc.).
- Hotkeys are global and may interfere with other applications.
- Admin rights might be needed to kill some processes.

---

## 📜 License

Free to use. Customize and improve as you like!
