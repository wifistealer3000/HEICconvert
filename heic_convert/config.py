from pathlib import Path

DOWNLOADS_DIR = Path.home() / "Downloads"
ORIGINALS_DIR = DOWNLOADS_DIR / "heic_originals"
WATCHED_EXTENSIONS = {".heic", ".heif"}
ORIGINALS_MAX_AGE_DAYS = 30
IDLE_CHECK_INTERVAL_SECONDS = 3600  # 1時間ごとにチェック
IDLE_THRESHOLD_SECONDS = 300  # 5分間操作なし→アイドル判定
DEBOUNCE_SECONDS = 1.5  # ファイル書き込み完了待ち
CONVERT_RETRY_COUNT = 3
CONVERT_RETRY_INTERVAL = 1.0  # 秒
APP_NAME = "HEIC Converter"
