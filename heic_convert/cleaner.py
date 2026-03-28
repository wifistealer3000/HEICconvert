import ctypes
import ctypes.wintypes
import logging
import time
from threading import Thread

from heic_convert.config import (
    ORIGINALS_DIR,
    ORIGINALS_MAX_AGE_DAYS,
    IDLE_CHECK_INTERVAL_SECONDS,
    IDLE_THRESHOLD_SECONDS,
)

log = logging.getLogger(__name__)


class _LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.wintypes.UINT),
        ("dwTime", ctypes.wintypes.DWORD),
    ]


def _get_idle_seconds() -> float:
    lii = _LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(_LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0


def _cleanup_old_files() -> None:
    if not ORIGINALS_DIR.exists():
        return
    now = time.time()
    max_age = ORIGINALS_MAX_AGE_DAYS * 86400
    for f in ORIGINALS_DIR.iterdir():
        if f.is_file() and (now - f.stat().st_mtime) > max_age:
            try:
                f.unlink()
                log.info("古いファイルを削除: %s", f.name)
            except OSError as e:
                log.warning("削除失敗: %s - %s", f.name, e)
            time.sleep(0.1)  # I/Oスパイク防止


def _cleaner_loop(stop_event) -> None:
    while not stop_event.is_set():
        stop_event.wait(IDLE_CHECK_INTERVAL_SECONDS)
        if stop_event.is_set():
            break
        if _get_idle_seconds() >= IDLE_THRESHOLD_SECONDS:
            log.info("アイドル検知 → クリーンアップ実行")
            _cleanup_old_files()


def start_cleaner(stop_event) -> Thread:
    t = Thread(target=_cleaner_loop, args=(stop_event,), daemon=True)
    t.start()
    return t
