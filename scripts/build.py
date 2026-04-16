"""
Build script for creating Telegraf.exe
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build_exe():
    """Build executable using PyInstaller"""

    # Get paths
    project_root = Path(__file__).parent.parent
    client_dir = project_root / "client"
    dist_dir = project_root / "dist"
    assets_dir = project_root / "assets"
    config_dir = project_root / "config"
    icon_path = assets_dir / "telegraf.ico"

    # Check if icon exists
    if not icon_path.exists():
        print("[WARNING] Icon not found, creating it...")
        os.system(f'python "{project_root / "scripts" / "create_icon.py"}"')

    # PyInstaller arguments
    args = [
        str(client_dir / "main.py"),
        "--name=Telegraf",
        f"--distpath={dist_dir}",
        "--onefile",
        "--windowed",
        f"--icon={icon_path}" if icon_path.exists() else "--icon=NONE",
        f"--add-data={config_dir};config",
        f"--add-data={assets_dir};assets",
        "--hidden-import=PyQt6",
        "--hidden-import=websockets",
        "--hidden-import=cryptography",
        "--clean",
        "--noconfirm"
    ]

    print("[BUILD] Building Telegraf.exe...")
    print(f"[BUILD] Output directory: {dist_dir}")

    try:
        PyInstaller.__main__.run(args)
        print("[OK] Build completed successfully!")
        print(f"[OK] Executable: {dist_dir / 'Telegraf.exe'}")
        return True
    except Exception as e:
        print(f"[ERROR] Build failed: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
