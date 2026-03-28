import sys
import winreg
from pathlib import Path

_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
_REG_NAME = "HEICConverter"


def _get_command() -> str:
    script = Path(__file__).resolve().parent.parent / "run.pyw"
    pythonw = Path(sys.executable).parent / "pythonw.exe"
    return f'"{pythonw}" "{script}"'


def is_registered() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, _REG_NAME)
            return True
    except FileNotFoundError:
        return False


def register() -> None:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, _REG_NAME, 0, winreg.REG_SZ, _get_command())


def unregister() -> None:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, _REG_NAME)
    except FileNotFoundError:
        pass
