import logging
import sys
from queue import Queue
from threading import Event

from heic_convert.config import ORIGINALS_DIR
from heic_convert.watcher import start_watcher
from heic_convert.converter import start_converter
from heic_convert.cleaner import start_cleaner
from heic_convert.tray import run_tray

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def main() -> None:
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)

    stop_event = Event()
    queue: Queue = Queue()

    observer = start_watcher(queue)
    converter_thread = start_converter(queue, stop_event)
    cleaner_thread = start_cleaner(stop_event)

    log.info("HEIC Converter 起動")

    def shutdown():
        log.info("シャットダウン中...")
        stop_event.set()
        observer.stop()
        queue.put(None)  # 変換ワーカー終了シグナル
        observer.join(timeout=3)
        converter_thread.join(timeout=3)
        cleaner_thread.join(timeout=3)

    try:
        run_tray(shutdown)
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()
