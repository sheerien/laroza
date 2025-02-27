from dataclasses import dataclass
from typing import List, Dict

from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser

from laroza_ramadan.helpers import (
    get_domain,
    LAROZA_OUTPUT_DIR,
    scraper,
    download_video,
    save_to_json,
    read_data_from_json_file,
    vk_extract_url
)
from laroza_ramadan.settings import settings, headers


@dataclass
class Episode:
    ep_number: int
    ep_url: str

@dataclass
class Series:
    name: str
    episodes: List[Episode]


def fetch_series_data() -> List[Dict]:
    """
    Fetches series data including episodes and returns a list of dictionaries.
    """
    series_list = scraper.fetch_series_list(settings.LAROZA_SITE_SERIES_LIST_URL, headers)
    data_eps = []
    
    if series_list:
        for series in series_list:
            episodes_data = scraper.fetch_episodes(series, headers)
            data_eps.append(episodes_data)
            print("\n", episodes_data)
    
    return data_eps


def extract_episode_embeds(episode_data: List[Series]) -> List[Dict]:
    """
    Extracts embed links from the last episode of each series.
    """
    eps_embeds = []
    
    for i, series in enumerate(episode_data, start=1):
        print()
        if series.episodes:
            last_episode = series.episodes[-1]
            print(series.name)
            print(last_episode["ep_url"])
            embeds = scraper.extract_embeds(url=last_episode["ep_url"], headers=headers)
            eps_embeds.append({
                "id": i,
                "ep_number": last_episode["ep_number"],
                "name": series.name,
                "last_ep_url": last_episode["ep_url"],
                "embeds": embeds
            })
            print("\n", embeds)
    
    return eps_embeds


def main():
    """
    Main function to orchestrate fetching and processing of series data.
    """
    data_eps = fetch_series_data()
    if data_eps:
        save_to_json(data_eps, f"{LAROZA_OUTPUT_DIR}series_list.json")
    
        data_episode = read_data_from_json_file(f"{LAROZA_OUTPUT_DIR}series_list.json")
        episode_data = [Series(**item) for item in data_episode]
    
        eps_embeds = extract_episode_embeds(episode_data)
        save_to_json(eps_embeds, f"{LAROZA_OUTPUT_DIR}embeds_list.json")


if __name__ == "__main__":
    main()
    
    @dataclass
    class Episode:
        id: int
        ep_number: int
        name: str
        last_ep_url: str
        embeds: List[str]


    data_eps = read_data_from_json_file(f"{LAROZA_OUTPUT_DIR}embeds_list.json")

    data_episodes: List[Episode]= [Episode(**item) for item in data_eps]

    data_players= []
    for d_ep in data_episodes:
        print("=" * 20)
        print(d_ep.name)
        sub_players = []
        if d_ep.embeds:
            for emb in d_ep.embeds:
                # print(emb)
                if "uqload" in emb:
                    print(emb)
                    print()
                    mp4 = scraper.fetch_uqload_mp4_links(emb, headers)
                    print(mp4)
                    if mp4:
                        sub_players.append(mp4)
                elif "vk.com" in emb:
                    print(emb)
                    print()
                    vk = vk_extract_url(emb)
                    if vk:
                        sub_players.append(vk)
                    print(vk)
                elif "ok.ru" in emb:
                    print(emb)
                    if emb:
                        sub_players.append(emb)
                else:
                    print(emb)
                    print()
                    m3u8 = scraper.extract_and_print_media_url(emb, headers)
                    if m3u8:
                        sub_players.append(m3u8)
                    print(m3u8)
        print()
        print(sub_players)
        data_players.append({"ep_name": d_ep.name, "season":1, "ep_number": d_ep.ep_number, "players": sub_players})

    if data_players:
        for d_player in data_players:
            print()
            print(d_player)
    
    save_to_json(data_players, f"{LAROZA_OUTPUT_DIR}players_list.json")
    
    # Define a data class to structure the episode data
    @dataclass
    class Episode:
        ep_name: str  # Name of the episode
        season: int   # Season number
        ep_number: int  # Episode number
        players: List[str]  # List of video player URLs

    data_players = read_data_from_json_file(f"{LAROZA_OUTPUT_DIR}players_list.json")

    episodes: List[Episode] = [Episode(**item) for item in data_players]


    for ep in episodes:
        print()
        print(ep.ep_name)
        print(ep.season)
        print(ep.ep_number)
        if ep.players:
            print()
            print(ep.players[0])
            download_video(ep.players[0], ep.ep_name, season=ep.season, episode=ep.ep_number)


