import os
import subprocess
import logging

from PIL import Image, ImageDraw, ImageFont
from pystray import Icon, Menu, MenuItem

from heic_convert.config import DOWNLOADS_DIR, ORIGINALS_DIR, APP_NAME
from heic_convert.startup import is_registered, register, unregister

log = logging.getLogger(__name__)


def _create_icon_image() -> Image.Image:
    """32x32のシンプルなアイコンをプログラム生成。"""
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 背景円
    draw.ellipse([2, 2, 29, 29], fill=(70, 130, 230))
    # "H" の文字
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    draw.text((8, 4), "H", fill="white", font=font)
    return img


def _open_folder(path):
    if path.exists():
        subprocess.Popen(["explorer", str(path)])


def run_tray(shutdown_callback) -> None:
    """システムトレイアイコンを表示（メインスレッドでブロック）。"""

    def on_open_downloads(icon, item):
        _open_folder(DOWNLOADS_DIR)

    def on_open_originals(icon, item):
        ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
        _open_folder(ORIGINALS_DIR)

    def on_toggle_startup(icon, item):
        if is_registered():
            unregister()
        else:
            register()

    def on_exit(icon, item):
        icon.stop()
        shutdown_callback()

    def startup_checked(item):
        return is_registered()

    menu = Menu(
        MenuItem("ダウンロードフォルダを開く", on_open_downloads),
        MenuItem("変換元フォルダを開く", on_open_originals),
        Menu.SEPARATOR,
        MenuItem("スタートアップに登録", on_toggle_startup, checked=startup_checked),
        Menu.SEPARATOR,
        MenuItem("終了", on_exit),
    )

    icon = Icon(APP_NAME, _create_icon_image(), APP_NAME, menu)
    icon.run()
