import yt_dlp
import os

def get_default_download_path():
    """Returns the default Downloads directory path for the current OS."""
    home = os.path.expanduser("~")  # Get the home directory
    if os.name == "nt":  # Windows
        return os.path.join(home, "Downloads")
    else:  # macOS & Linux
        return os.path.join(home, "Downloads")

def download_video(url: str, series_name: str, output_folder: str = None, referer: str = None, season: int = 1, episode: int = 1):
    """
    Downloads a video using yt-dlp with the highest available quality.

    :param url: The video URL to download.
    :param series_name: The name of the series to include in the filename.
    :param output_folder: The directory where the file will be saved. If None, uses the system's default Downloads folder.
    :param referer: The referer URL to bypass restrictions (optional).
    :param season: The season number for naming the file (default: 1).
    :param episode: The episode number for naming the file (default: 1).
    """

    # If output_folder is not provided, use the system's default Downloads folder
    if output_folder is None:
        output_folder = get_default_download_path()

    # Define the Ramadan series folder inside the output folder
    ramadan_folder = os.path.join(output_folder, "ramadan_series")

    # Ensure the Ramadan series folder exists
    os.makedirs(ramadan_folder, exist_ok=True)

    # Format episode and season numbers for naming convention (e.g., MySeries.S01.E05)
    episode_str = f"E{episode}" if episode >= 10 else f"E0{episode}"
    season_str = f"S{season:02d}"
    filename_template = f"{series_name}.{season_str}.{episode_str}.%(ext)s"

    # yt-dlp options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and audio available
        'outtmpl': os.path.join(ramadan_folder, filename_template),  # Output filename format
        'merge_output_format': 'mp4',  # Ensure the final file is in MP4 format
        'nocheckcertificate': True,  # Bypass SSL certificate verification
        'quiet': False,  # Show detailed output
        'noprogress': False,  # Display download progress
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],  # Ensure MP4 format after merging
        'http_headers': {
            'Referer': referer if referer else '',  # Add referer to bypass restrictions
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',  # Fake browser user-agent
        }
    }

    try:
        # Initialize yt-dlp with the options and start the download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✅ Download completed successfully! Saved in: {ramadan_folder}")
    except Exception as e:
        # Handle errors and print the error message
        print(f"❌ An error occurred during download: {e}")

# Example usage
# url = r"https://example.com/video.mp4"
# series_name = "Example_Series"
# download_video(url=url, series_name=series_name, referer="https://example.com")

