from bs4 import BeautifulSoup

from html_utils import HTMLUtils
from page_constants import *
from pdf_writer_v2 import PDFWriter


def write_cover():
    writer.write_cover(COVER_IMAGE,
                       COVER_IMAGE_WIDTH,
                       COVER_TEXT,
                       COVER_TEXT_Y_CM,
                       COVER_SUB_TEXT,
                       COVER_SUB_TEXT_Y_CM,
                       DEFAULT_FONT_BOLD,
                       COVER_FONT_SIZE,
                       COVER_FONT_COLOUR,
                       COVER_LINK)


def get_all_episodes() -> list:
    next_page_url = START_URL
    all_episodes: list = []

    temp = 1

    while next_page_url is not None:
        print(f'Getting data for {next_page_url}')
        current_html = HTMLUtils.get_html_from_url(next_page_url)
        soup = BeautifulSoup(current_html, 'html.parser')
        all_episodes.extend(HTMLUtils.get_episodes_from_page(soup))
        next_page_url = HTMLUtils.get_next_page_url(soup)
        temp += 1
        # next_page_url = None if temp == 5 else next_page_url

    return all_episodes


def write_toc(all_episodes: list):
    writer.write_toc(all_episodes,
                     TOC_TEXT,
                     DEFAULT_FONT_BOLD,
                     TOC_FONT_SIZE,
                     TOC_FONT_COLOUR,
                     TOC_SPACING_DELTA)


def create_magazine():
    write_cover()
    all_episodes = get_all_episodes()
    write_toc(all_episodes)
    build_pages(all_episodes)


def build_pages(all_episodes: list):
    for episode in all_episodes:
        retry = True
        retry_count = 0
        while retry:
            try:
                print(f'{episode.episode_num} [{episode.title}]')
                writer.insert_image_from_ulr_centred(episode.cover, EPISODE_IMAGE_WIDTH, episode.mp3)
                writer.write_text_to_page_centered_x(episode.title,
                                                     EPISODE_TEXT_Y_CM,
                                                     DEFAULT_FONT_BOLD,
                                                     EPISODE_FONT_SIZE,
                                                     EPISODE_FONT_COLOUR)
                writer.write_listen_image(episode.mp3,
                                          LISTEN_IMAGE,
                                          LISTEN_IMAGE_WIDTH,
                                          LISTEN_IMAGE_Y)
                writer.new_page()
                retry = False
            except Exception as e:
                print(f'EXCEPTION !! Thrown processing:\n{episode.to_string()}')
                print(f'EXCEPTION DETAILS\n=================\n{e}\n=================\n')
                retry_count += 1
                if retry_count > 5:
                    SystemExit(1)


writer = PDFWriter()
create_magazine()
writer.save_and_close_pdf()

print("All done !")
