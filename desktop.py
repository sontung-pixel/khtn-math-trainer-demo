import ctypes
import sys
from pathlib import Path

import webview


def resource_path(name: str) -> Path:
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return root / name


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except (AttributeError, OSError):
        pass
    page = resource_path("web/index.html").as_uri()
    webview.create_window(
        "KHTN Math Trainer",
        page,
        width=1280,
        height=820,
        min_size=(1050, 680),
        background_color="#080d1a",
    )
    webview.start(debug=False)
