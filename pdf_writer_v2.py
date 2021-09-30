import io
import os
import tempfile

import numpy as np
import requests
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from page_constants import *

PAGE_HEIGHT = 30
PAGE_WIDTH = 21


class PDFWriter:
    def __init__(self):
        self.canvas = Canvas(f'{PDF_LOCATION}{os.path.sep}{PDF_NAME}', pagesize=A4)
        print(f'{self.canvas.getAvailableFonts()}')

    def new_page(self):
        self.canvas.showPage()

    def write_listen_image(self,
                           link_url: str,
                           listen_image_url: str,
                           listen_image_width: int,
                           listen_image_y: int):
        page_width, page_height = A4
        image_x = (page_width - listen_image_width) / 2
        self.insert_image_from_ulr_with_link(listen_image_url,
                                             listen_image_width,
                                             image_x,
                                             listen_image_y,
                                             link_url,
                                             show_boundary=False)

    def write_text_to_page(self,
                           text: str,
                           font_name: str,
                           font_size: int,
                           font_colour: any,
                           x_cm: int,
                           y_cm: int):
        canvas_text = self.canvas.beginText(x_cm * cm, y_cm * cm)
        canvas_text.setFont(font_name, font_size)
        canvas_text.setFillColor(font_colour)
        canvas_text.textLine(text)
        self.canvas.drawText(canvas_text)

    def write_text_to_page_centered_x(self,
                                      text: str,
                                      y_cm: int,
                                      font: str,
                                      font_size: int,
                                      font_colour: colors.HexColor):
        text_width = self.canvas.stringWidth(text, font, font_size)
        page_width, page_height = A4
        text_x = (page_width - text_width) / 2
        canvas_text = self.canvas.beginText(text_x, y_cm)
        canvas_text.setFont(font, font_size)
        canvas_text.setFillColor(font_colour)
        canvas_text.textLine(text)
        self.canvas.drawText(canvas_text)

    def write_cover(self,
                    image_url: str,
                    image_width: int,
                    text: str,
                    text_y_cm: int,
                    sub_text: str,
                    sub_text_y_cm: int,
                    font: str,
                    font_size: int,
                    font_colour: colors.HexColor,
                    link_url: str = None):
        print('Writing main cover')
        self.insert_image_from_ulr_centred(image_url, image_width, link_url)

        self.write_text_to_page_centered_x(text, text_y_cm, font, font_size, font_colour)
        self.write_text_to_page_centered_x(sub_text, sub_text_y_cm, font, font_size, font_colour)

        self.new_page()

    def write_toc(self,
                  episodes: list,
                  toc_text: str,
                  toc_font: str,
                  toc_font_size: int,
                  toc_font_colour: colors.HexColor,
                  toc_spacing_delta: float):
        x = 1
        current_y = PAGE_HEIGHT - 1

        self.write_text_to_page(toc_text, toc_font, toc_font_size + 4, toc_font_colour, 8, current_y)
        current_y -= toc_spacing_delta

        for episode in episodes:

            if current_y == 0:
                current_y = PAGE_HEIGHT - 1
                self.new_page()

            toc_info = f'{episode.title}'
            print(f'TOC x,y: {x}, {current_y}')
            self.write_text_to_page(f'{toc_info}',
                                    toc_font,
                                    toc_font_size,
                                    toc_font_colour,
                                    x,
                                    current_y)
            current_y -= toc_spacing_delta

        self.new_page()

    def insert_image_from_ulr_with_link(self, image_url: str, required_width: int, image_x: int, image_y: int,
                                        link_url: str = None, show_boundary: bool = True):
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))

        # Convert it if we need to
        image_format = image_url[image_url.rindex(".") + 1:].lower()
        if image_format == "jpg" or image_format == "jpeg":
            a = np.asarray(image)
            image = Image.fromarray(a)
            image_format = "png"

        width_percent = (required_width / float(image.size[0]))
        height_size = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((required_width, height_size), Image.NEAREST)

        tmp = tempfile.NamedTemporaryFile()
        image.save(tmp.name, format=image_format)
        resized_image = ImageReader(tmp)

        self.canvas.drawImage(resized_image, image_x, image_y, required_width, height_size, preserveAspectRatio=True,
                              showBoundary=show_boundary)

        if image_url is not None and image_url.strip() != "":
            link_rect = (int(image_x), int(image_y), (int(image_x) + required_width), (int(image_y) + height_size))
            self.canvas.linkURL(link_url, link_rect, relative=0, thickness=0)

    def insert_image_from_ulr_centred(self, url: str, required_width: int, link_url: str = None):
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))

        # Convert it if we need to
        image_format = url[url.rindex(".") + 1:].lower()
        if image_format == "jpg" or image_format == "jpeg":
            a = np.asarray(image)
            image = Image.fromarray(a)
            image_format = "png"

        width_percent = (required_width / float(image.size[0]))
        height_size = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((required_width, height_size), Image.NEAREST)

        tmp = tempfile.NamedTemporaryFile()
        image.save(tmp.name, format=image_format)
        resized_image = ImageReader(tmp)

        page_width, page_height = A4
        image_x = (page_width - required_width) / 2
        image_y = (page_height - height_size) / 2
        self.canvas.drawImage(resized_image, image_x, image_y, required_width, height_size, preserveAspectRatio=True,
                              showBoundary=True)

        if url is not None and url.strip() != "":
            link_rect = (int(image_x), int(image_y), (int(image_x) + required_width), (int(image_y) + height_size))
            self.canvas.linkURL(link_url, link_rect, relative=0, thickness=0)

    def save_and_close_pdf(self):
        self.canvas.save()
