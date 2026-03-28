import logging
from pathlib import Path
from queue import Queue
from threading import Timer

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent

from heic_convert.config import DOWNLOADS_DIR, WATCHED_EXTENSIONS, DEBOUNCE_SECONDS

log = logging.getLogger(__name__)


class HEICHandler(FileSystemEventHandler):
    def __init__(self, queue: Queue):
        super().__init__()
        self._queue = queue
        self._timers: dict[str, Timer] = {}

    def _schedule(self, path: Path) -> None:
        key = str(path).lower()
        # 既存タイマーをキャンセル（デバウンス）
        if key in self._timers:
            self._timers[key].cancel()
        timer = Timer(DEBOUNCE_SECONDS, self._enqueue, args=(path, key))
        timer.daemon = True
        timer.start()
        self._timers[key] = timer

    def _enqueue(self, path: Path, key: str) -> None:
        self._timers.pop(key, None)
        if path.exists():
            log.info("検知: %s", path.name)
            self._queue.put(path)

    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() in WATCHED_EXTENSIONS:
            self._schedule(path)

    def on_moved(self, event: FileMovedEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.dest_path)
        if path.suffix.lower() in WATCHED_EXTENSIONS:
            self._schedule(path)


def start_watcher(queue: Queue) -> Observer:
    """ダウンロードフォルダの監視を開始する。"""
    handler = HEICHandler(queue)
    observer = Observer()
    observer.schedule(handler, str(DOWNLOADS_DIR), recursive=False)
    observer.daemon = True
    observer.start()
    log.info("監視開始: %s", DOWNLOADS_DIR)
    return observer
