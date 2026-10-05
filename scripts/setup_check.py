from __future__ import annotations

import platform
import sys
from pathlib import Path


def main() -> None:
    print(f"Python: {platform.python_version()}")
    print(f"Executable: {sys.executable}")
    print(f"Current directory: {Path.cwd()}")
    print("Environment check complete.")


if __name__ == "__main__":
    main()
