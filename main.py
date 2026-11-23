import os
import shutil
from pathlib import Path

def main():
    bot_dir = Path(os.environ.get("MAKEFUN_BOT_DIR", "."))
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    src = bot_dir / "entry.png"
    dst = output_dir / "entry.png"
    
    if src.exists():
        shutil.copy(src, dst)
        print(f"Successfully copied {src} to {dst}")
    else:
        print(f"Source {src} not found!")

if __name__ == "__main__":
    main()
