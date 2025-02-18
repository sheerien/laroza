from typing import Final
import os

BASE_DIR: Final = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR: Final = os.path.join(BASE_DIR, "output")
LAROZA_OUTPUT_DIR: Final = os.path.join(OUTPUT_DIR, "laroza_")
DB_PATH: Final = os.path.join(BASE_DIR, "database.json")