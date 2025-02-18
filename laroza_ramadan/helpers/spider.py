import re
from typing import List, Optional, Dict
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser

class LarozaScraper:
    """
    A utility class for scraping Laroza, providing methods to extract MP4 URLs,
    fetch pagination details, and extract series and episode data.
    """
    
    def __init__(self):
        """
        Initializes the LarozaScraper with an HTMLSession.
        """
        self.session = HTMLSession()
    
    def extract_mp4s(self, text: str) -> Optional[List[str]]:
        """
        Extracts MP4 URLs from the provided text.

        Args:
            text (str): The input text containing possible MP4 URLs.

        Returns:
            Optional[List[str]]: A list of MP4 URLs if found, otherwise None.
        """
        try:
            pattern = r"https?://.*?\\.mp4"
            mp4_urls = re.findall(pattern, text)
            return mp4_urls if mp4_urls else None
        except Exception as e:
            print(f"Error extracting MP4 URLs: {e}")
            return None




# Example usage
scraper = LarozaScraper()