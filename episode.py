from bs4 import BeautifulSoup
from page_constants import MP3_MARKERS


class Episode:
    def __init__(self, current_url: str, current_pic: str):
        self.url: str = current_url
        self.cover: str = current_pic
        self.title: str = ""
        self.description: str = ""
        self.mp3: str = ""
        self.episode_num: str = ""
        self.add_episode_details()

    def to_string(self) -> str:
        data = f'URL: {self.url}\n'
        data += f'Cover Image: {self.cover}\n'
        data += f'Title: {self.title}\n'
        data += f'Description: {self.description}\n'
        data += f'MP3: {self.mp3}\n'
        data += f'Episode: {self.episode_num}\n'
        return data

    def add_episode_details(self):
        from html_utils import HTMLUtils
        current_html = HTMLUtils.get_html_from_url(self.url)
        soup = BeautifulSoup(current_html, 'html.parser')

        my_divs = soup.find_all("div", {"class": "post-block-editorial-title"})
        self.title = my_divs[0].text.strip()

        pos = self.title.find("–")
        self.episode_num = self.title[:pos].strip()
        pos = self.episode_num.find(":")
        if pos != -1:
            self.episode_num = self.episode_num[:pos].strip()

        my_divs = soup.find_all("p")
        self.description = my_divs[0].text.strip()
        pics = my_divs[0].find_all("img")
        if len(pics) > 0:
            self.cover = pics[0].get("src")
        if self.description == "":  # Happens on later pages
            self.description = my_divs[1].text.strip()
        for div in my_divs:
            if self.mp3 is not None and self.mp3 != "":
                break
            current_paragraph = div.text.strip()

            mp3s = div.find_all("a")
            # Some do not have the "Download..." text
            for mp3 in mp3s:
                if (mp3 is not None or mp3.text.strip() != "") and \
                        ".mp3" in mp3.text.strip().lower():
                    self.mp3 = mp3.text.strip()
                    break
            if self.mp3 is "":  # Not found the MP3 link yet
                for marker in MP3_MARKERS:
                    if marker.lower() in current_paragraph.lower():
                        urls = div.find_all("a")
                        if len(urls) != 0:
                            self.mp3 = urls[0].get("href").strip()
                            break

        if not self.mp3.endswith("mp3") and not self.mp3.endswith("mp3/"):
            print(f'\tWeird MP3 Link:\n\t\tMP3 Link - {self.mp3}\n\t\tPage - {self.url}')
            if self.mp3 == "":
                print(f'\tNo link found:\n\t\tPage - {self.url}')
                if "mp3" in current_html.lower():
                    print(f'!!! mp3 found in html for page:\n{current_html}')
