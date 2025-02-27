import re
from typing import Optional
from urllib.parse import urlparse


def get_domain(url: str) -> str:
    """
    Extracts the domain with the scheme (protocol) from a given URL.

    Args:
        url (str): The input URL.

    Returns:
        str: The full domain with protocol (e.g., 'https://example.com').

    Raises:
        ValueError: If the URL is invalid or does not contain a netloc.
    """
    parsed_url = urlparse(url)

    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid URL: Scheme or domain is missing.")

    return f"{parsed_url.scheme}://{parsed_url.netloc}"



import json


def save_to_json(data: list, filename: str) -> None:
    """
    Saves the given data to a JSON file.

    Args:
        data (list): The data to save.
        filename (str): The name of the JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print()
        print(f"{filename} created is done !")



def read_data_from_json_file(filename: str) -> dict:
    """
    Reads data from a JSON file.

    Args:
        filename: The name of the JSON file (without the .json extension).

    Returns:
        The parsed JSON data as a dictionary, or None if an error occurs.
    """
    try:
        with open(f"{filename}", encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None


def vk_extract_url(original_url: str) -> Optional[str]:
    """
    Extracts the URL of the format 'https://vk.com/video<numeric>_<numeric>' 
    from the given original URL using regular expressions.

    Args:
        original_url (str): The original URL from which to extract the desired URL.

    Returns:
        Optional[str]: The extracted URL if found, else None.
    """
    try:
        # Define a regex pattern to match the desired URL format
        pattern = r"oid=(\d{9}).*id=(\d{9})"

        # Use re.search() to find the pattern in the original URL
        match = re.search(pattern, original_url)

        # If a match is found, construct and return the extracted URL
        if match:
            extracted_url = fr"https://vk.com/video{match.group(1)}_{match.group(2)}"
            return extracted_url
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None