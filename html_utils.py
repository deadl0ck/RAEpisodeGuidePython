import requests
from utils import Utils
from episode import Episode


class HTMLUtils:
    @staticmethod
    def get_html_from_url(url: str) -> str:
        return requests.get(url).text

    @staticmethod
    def get_next_page_url(soup: any) -> any:
        my_divs = soup.find_all("div", {"class": "next-page-graphic"})
        for div in my_divs:
            urls = div.find_all("area")
        if len(urls) < 1:
            return None

        return urls[0].get("href")

    @staticmethod
    def get_episodes_from_page(soup: any) -> list:
        my_divs = soup.find_all("div", {"class": "previous-posts-container"})
        for div in my_divs:
            urls = div.find_all("a")
            pics = div.find_all("img")

        if len(urls) != len(pics):
            Utils.print_error_and_exit("Different number of URLs and Covers found - aborting")

        episodes: list = []
        for i in range(len(urls)):
            link = urls[i].get("href")
            cover = pics[i].get("src")
            if link.strip() != "" and cover.strip() != "":
                episodes.append(Episode(link, cover))
        return episodes
