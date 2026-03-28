# HEIC Converter

ダウンロードフォルダを監視し、HEIC/HEIFファイルを自動でPNGに変換するWindows常駐ツールです。

---

## 機能

- **自動変換**: ダウンロードフォルダに保存されたHEIC/HEIFファイルを即座にPNGへ変換
- **タスクトレイ常駐**: システムトレイにアイコンを表示し、右クリックメニューから操作可能
- **スタートアップ登録**: Windows起動時に自動で起動するよう設定可能
- **ファイル名重複処理**: 同名のPNGが存在する場合、自動で連番を付与（`photo_1.png`, `photo_2.png`...）
- **トースト通知**: 変換失敗やファイル名変更時にWindowsの通知で知らせる
- **自動クリーンアップ**: 変換済みの元ファイルを`heic_originals`フォルダに保管し、30日経過後にシステムがアイドル状態の時に自動削除
- **低負荷設計**: イベント駆動型でアイドル時のCPU使用率はほぼゼロ

## 必要環境

- Windows 10/11
- Python 3.10以上

## インストール

```bash
git clone https://github.com/wifistealer3000/HEICconvert.git
cd HEICconvert
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

## 使い方

### 起動

```bash
venv\Scripts\pythonw.exe run.pyw
```

起動するとタスクトレイにアイコン（青い丸に「H」）が表示されます。

### トレイメニュー（右クリック）

| メニュー | 説明 |
|---|---|
| ダウンロードフォルダを開く | 監視対象のダウンロードフォルダをエクスプローラーで開く |
| 変換元フォルダを開く | 変換済みのHEIC/HEIFファイルの保管先を開く |
| スタートアップに登録 | Windows起動時に自動実行するかどうかを切り替え |
| 終了 | アプリケーションを終了 |

### 動作の流れ

1. ダウンロードフォルダに`.heic`または`.heif`ファイルが保存される
2. ファイルの書き込み完了を待つ（1.5秒のデバウンス）
3. PNGに変換し、同じフォルダに出力
4. 元のHEIC/HEIFファイルを`Downloads\heic_originals`フォルダに移動
5. 30日以上経過した元ファイルは、PCがアイドル状態の時に自動削除

### 通知が出るケース

- **ファイル名変更時**: 同名のPNGが既に存在し、連番に変更された場合
- **変換失敗時**: ファイルの破損やアクセスエラーなどで変換できなかった場合

## フォルダ構成

```
Downloads/
├── photo.png              ← 変換後のPNG
├── photo.heic             ← (変換前、変換後は移動される)
└── heic_originals/        ← 変換済みの元ファイルの保管先
    └── photo.heic
```

## アンインストール

1. トレイメニューから「スタートアップに登録」のチェックを外す
2. トレイメニューから「終了」を選択
3. プロジェクトフォルダを削除

---

# HEIC Converter (English)

A lightweight Windows system tray application that monitors your Downloads folder and automatically converts HEIC/HEIF files to PNG.

## Features

- **Auto-conversion**: Instantly converts HEIC/HEIF files saved to your Downloads folder into PNG
- **System tray**: Runs quietly in the system tray with a right-click context menu
- **Startup registration**: Optionally launch at Windows startup
- **Duplicate handling**: Automatically appends sequential numbers when a PNG with the same name already exists (`photo_1.png`, `photo_2.png`...)
- **Toast notifications**: Notifies you on conversion failure or filename changes
- **Auto-cleanup**: Moves originals to `heic_originals` subfolder; deletes files older than 30 days when the system is idle
- **Low overhead**: Event-driven design with near-zero CPU usage when idle

## Requirements

- Windows 10/11
- Python 3.10+

## Installation

```bash
git clone https://github.com/wifistealer3000/HEICconvert.git
cd HEICconvert
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

## Usage

### Launch

```bash
venv\Scripts\pythonw.exe run.pyw
```

A tray icon (blue circle with "H") will appear in the system tray.

### Tray Menu (Right-click)

| Menu Item | Description |
|---|---|
| Open Downloads Folder | Open the monitored Downloads folder in Explorer |
| Open Originals Folder | Open the folder containing converted HEIC/HEIF originals |
| Register at Startup | Toggle auto-launch at Windows startup |
| Exit | Quit the application |

### How It Works

1. A `.heic` or `.heif` file is saved to your Downloads folder
2. The app waits for the file to finish writing (1.5s debounce)
3. Converts it to PNG in the same folder
4. Moves the original HEIC/HEIF file to `Downloads\heic_originals`
5. Originals older than 30 days are automatically deleted when the PC is idle

### When You Get Notifications

- **Filename changed**: A PNG with the same name already existed, so a sequential number was added
- **Conversion failed**: The file was corrupted or could not be accessed

## Folder Structure

```
Downloads/
├── photo.png              ← Converted PNG
├── photo.heic             ← (Before conversion; moved after)
└── heic_originals/        ← Storage for converted originals
    └── photo.heic
```

## Uninstall

1. Uncheck "Register at Startup" from the tray menu
2. Click "Exit" from the tray menu
3. Delete the project folder
