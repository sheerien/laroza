from laroza_ramadan.helpers import (
    get_domain,
    LAROZA_OUTPUT_DIR,
    scraper,
    download_video,
    save_to_json,
    read_data_from_json_file,
)
from laroza_ramadan.settings import settings
import re
from typing import List, Optional, Dict
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser

session = HTMLSession()