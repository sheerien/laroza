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
import re
from typing import List, Dict, Set
from httpx_html import HTMLSession
from httpx import RequestError
from selectolax.parser import HTMLParser
from dataclasses import dataclass


session = HTMLSession()

series_list = scraper.fetch_series_list(settings.LAROZA_SITE_SERIES_LIST_URL, headers)

def main():
    """
    Main function to fetch and display episode data.
    """
    data_eps = []
    series_list = scraper.fetch_series_list(settings.LAROZA_SITE_SERIES_LIST_URL, headers)
    if series_list:
        for series in series_list:
            episodes_data = scraper.fetch_episodes(series, headers)
            data_eps.append(episodes_data)
            print("\n", episodes_data)
    return data_eps if data_eps else []

if __name__ == "__main__":
    data_eps = main()
    for data in data_eps:
        print()
        print(data)
    
    save_to_json(data_eps, f"{LAROZA_OUTPUT_DIR}series_list.json")
    @dataclass
    class Episode:
        ep_number: int
        ep_url: str

    @dataclass
    class Series:
        name: str
        episodes: List[Episode]
        
    data_episode = read_data_from_json_file(f"{LAROZA_OUTPUT_DIR}series_list.json")
    
    episode_data: List[Series] = [Series(**item) for item in data_episode]
    
    eps_embeds = []
    for i, ep in enumerate(episode_data):
        print()
        if ep.episodes:
            print(ep.name)
            print(ep.episodes[-1]["ep_url"])
            embeds = scraper.extract_embeds(url=ep.episodes[-1]["ep_url"], headers=headers)
            eps_embeds.append({"id": int(i+1), "ep_number": ep.episodes[-1]["ep_number"], "name": ep.name, "last_ep_url": ep.episodes[-1]["ep_url"], "embeds": embeds})
            print()
            print(embeds)
            
    save_to_json(eps_embeds, f"{LAROZA_OUTPUT_DIR}embeds_list.json")
    
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
        data_players.append({"ep_name": d_ep.name, "ep_number": d_ep.ep_number, "players": sub_players})

    if data_players:
        for d_player in data_players:
            print()
        print(d_player)