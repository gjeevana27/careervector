from pathlib import Path
import streamlit as st

# Project root
ROOT = Path(__file__).resolve().parents[2]

# assets/icons folder
ICON_DIR = ROOT / "assets" / "icons"


def icon(name: str, size: int = 28):

    icon_path = ICON_DIR / f"{name}.svg"

    if icon_path.exists():
        st.image(str(icon_path), width=size)
    else:
        st.error(f"Icon not found: {icon_path}")