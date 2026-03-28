import shutil
import time
import logging
from pathlib import Path
from queue import Queue, Empty
from threading import Thread

import pillow_heif
from PIL import Image

from heic_convert.config import (
    ORIGINALS_DIR,
    CONVERT_RETRY_COUNT,
    CONVERT_RETRY_INTERVAL,
)
from heic_convert.notifier import notify_renamed, notify_error

pillow_heif.register_heif_opener()
log = logging.getLogger(__name__)


def _find_available_path(base_path: Path) -> tuple[Path, bool]:
    """重複しないファイルパスを見つける。リネームした場合は(path, True)を返す。"""
    if not base_path.exists():
        return base_path, False
    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate, True
        counter += 1


def _convert_one(heic_path: Path) -> None:
    """1ファイルを変換する。"""
    png_base = heic_path.with_suffix(".png")
    png_path, renamed = _find_available_path(png_base)

    last_error = None
    for attempt in range(CONVERT_RETRY_COUNT):
        try:
            with Image.open(heic_path) as img:
                img.save(png_path, "PNG")
            break
        except Exception as e:
            last_error = e
            if attempt < CONVERT_RETRY_COUNT - 1:
                time.sleep(CONVERT_RETRY_INTERVAL)
    else:
        log.error("変換失敗: %s - %s", heic_path.name, last_error)
        notify_error(heic_path.name, str(last_error))
        return

    # 元ファイルを移動
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
    dest = ORIGINALS_DIR / heic_path.name
    dest_path, _ = _find_available_path(dest)
    shutil.move(str(heic_path), str(dest_path))

    log.info("変換完了: %s → %s", heic_path.name, png_path.name)
    if renamed:
        notify_renamed(heic_path.stem + ".png", png_path.name)


def converter_worker(queue: Queue, stop_event) -> None:
    """キューからファイルを取り出して変換するワーカー。"""
    while not stop_event.is_set():
        try:
            heic_path = queue.get(timeout=1.0)
        except Empty:
            continue
        if heic_path is None:  # 終了シグナル
            break
        try:
            _convert_one(heic_path)
        except Exception as e:
            log.error("予期しないエラー: %s - %s", heic_path.name, e)


def start_converter(queue: Queue, stop_event) -> Thread:
    """変換ワーカースレッドを開始する。"""
    t = Thread(target=converter_worker, args=(queue, stop_event), daemon=True)
    t.start()
    return t
