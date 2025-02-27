import re
from typing import List, Dict, Optional, Set
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser
from .helper import get_domain


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
        self.PLAYERS_NAMES = [
            "okprime",
            "vidspeeds",
            "vidroba",
            "uqload",
            "ok.ru",
            "vk",
        ]

    def extract_media_urls(self, text: str) -> Optional[List[str]]:
        """
        Extracts MP4 and M3U8 URLs from the provided text and classifies M3U8 URLs.

        Args:
            text (str): The input text containing possible MP4/M3U8 URLs.

        Returns:
            Tuple[Optional[List[str]], Optional[List[str]]]: 
            - First list: M3U8 URLs without extra parameters.
            - Second list: M3U8 URLs with additional parameters.
        """
        pattern = r"https?://\S+?\.(?:mp4|m3u8)(?:\?.*)?"
        urls = re.findall(pattern, text)

        if not urls:
            return None, None

        clean_urls = [url for url in urls if url.endswith(".m3u8")]
        full_urls = [url for url in urls if ".m3u8?" in url]

        return clean_urls if clean_urls else None, full_urls if full_urls else None


    def extract_mp4s(self, text: str) -> Optional[List[str]]:
        """
        Extracts MP4 URLs from the provided text.

        Args:
            text (str): The input text containing possible MP4 URLs.

        Returns:
            Optional[List[str]]: A list of MP4 URLs if found, otherwise None.
        """
        try:
            pattern = r"https?://.*?v.mp4"
            mp4_urls = re.findall(pattern, text)
            return mp4_urls if mp4_urls else None
        except Exception as e:
            print(f"Error extracting MP4 URLs: {e}")
            return None

    def fetch_series_list(
        self, url: str, headers: Dict[str, str]
    ) -> List[Dict[str, str]]:
        """
        Fetches a unique list of series names and URLs from the given site.

        Args:
            url (str): The URL of the series list page.
            headers (Dict[str, str]): The request headers.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing series names and URLs.
        """
        try:
            response = self.session.get(url=url, headers=headers)
            response.raise_for_status()  # Raise error for failed requests

            html = response.html.html
            parser = HTMLParser(html)

            all_series = parser.css_first("div.pm-category-description")
            if not all_series:
                raise ValueError("Could not find series container in the HTML.")

            anchors = all_series.css("a.icon-link")

            unique_series: Set[tuple] = set()  # To ensure uniqueness
            series_data: List[Dict[str, str]] = []

            for anchor in anchors:
                series_name = anchor.text().strip()
                series_url = anchor.attributes.get("href", "").strip()

                if series_name and series_url:  # Ensure no empty values
                    series_tuple = (series_name, series_url)
                    if series_tuple not in unique_series:
                        unique_series.add(series_tuple)
                        series_data.append(
                            {"series_name": series_name, "series_url": series_url}
                        )

            return series_data

        except RequestError as e:
            print(f"Request failed: {e}")
            return []
        except ValueError as e:
            print(f"Parsing error: {e}")
            return []

    def fetch_episodes(
        self, series_data: Dict[str, str], headers: Dict[str, str]
    ) -> Dict[str, List[Dict[str, str]]]:
        """
        Fetches the episode list from the given series URL.
        """
        try:
            resp = self.session.get(url=series_data["series_url"], headers=headers)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error fetching episodes: {e}")
            return {"name": series_data["series_name"], "episodes": []}

        parser = HTMLParser(resp.html.html)
        base_url = get_domain(series_data["series_url"])
        ul = parser.css_first("ul.pm-ul-browse-videos")
        if not ul:
            return {"name": series_data["series_name"], "episodes": []}

        episodes = [
            {
                "ep_number": i + 1,
                "ep_url": f"{base_url}/{li.css_first('a').attributes['href'].replace('video', 'play').strip()}",
            }
            for i, li in enumerate(ul.css("li"))
        ]

        return {"name": series_data["series_name"], "episodes": episodes}

    def extract_embeds(self, url: str, headers: Dict[str, str]) -> List[str]:
        """
        Extracts embed URLs from the given webpage based on supported player names.

        Args:
            url (str): The URL of the webpage to scrape.
            headers (Dict[str, str]): HTTP headers to use in the request.

        Returns:
            List[str]: A list of extracted embed URLs.
        """
        try:
            # Send a GET request to the URL
            resp = self.session.get(url=url, headers=headers)
            resp.raise_for_status()  # Ensure the request was successful

            # Parse the HTML content
            parser = HTMLParser(resp.html.html)

            # Find the first <ul> element with class 'WatchList'
            ul = parser.css_first("ul.WatchList")
            if not ul:
                return []  # Return an empty list if the element is not found

            # Extract embed URLs that match the supported players
            return [
                li.attributes["data-embed-url"].strip()
                for li in ul.css("li")
                if "data-embed-url" in li.attributes
                and any(
                    player in li.attributes["data-embed-url"]
                    for player in self.PLAYERS_NAMES
                )
            ]

        except Exception as e:
            print(f"An error occurred while extracting embed links: {e}")
            return []


    def extract_and_print_media_url(self, url: str, headers: Dict[str, str]) -> str:
        """
        Fetches a URL, extracts media URLs, and returns the most relevant one.
        """
        try:
            response = self.session.get(url=url, headers=headers)
            response.raise_for_status()
            text = response.text
            clean_urls, full_urls = self.extract_media_urls(text)
            if clean_urls:
                return clean_urls[0]
            if full_urls:
                sanitized_url = full_urls[0].replace('"}],', "") if '"}],' in full_urls[0] else full_urls[0]

                return sanitized_url
        except TypeError as e:
            print(f"TypeError occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return ""


    def fetch_uqload_mp4_links(self, url: str, headers: Dict[str, str]) -> str:
        """
        Fetches MP4 links from a given URL.
        """
        try:
            response = self.session.get(url=url, headers=headers)
            response.raise_for_status()
            html_content = response.html.html
            mp4 = self.extract_mp4s(str(html_content))
            return mp4[0] if mp4 else ""
        except Exception as e:
            print(f"Error fetching MP4 links: {e}")
            return []
        
        

    def close_session(self):
        """
        Closes the HTTP session to free resources.
        """
        self.session.close()


scraper = LarozaScraper()
