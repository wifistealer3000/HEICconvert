from winotify import Notification
from heic_convert.config import APP_NAME


def notify_renamed(original_name: str, new_name: str) -> None:
    toast = Notification(
        app_id=APP_NAME,
        title="ファイル名を変更しました",
        msg=f"{original_name} → {new_name}\n（同名ファイルが存在したため連番に変更）",
    )
    toast.show()


def notify_error(filename: str, error: str) -> None:
    toast = Notification(
        app_id=APP_NAME,
        title="変換に失敗しました",
        msg=f"{filename}: {error}",
    )
    toast.show()
