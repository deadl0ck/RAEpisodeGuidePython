from reportlab.lib import colors
from reportlab.lib.units import cm

START_URL = "http://retroasylum.com/category/all-posts/podcasts/"
MP3_MARKERS = ["Download the episode",
               "Dwonload the episode",
               "Download episode"]

PDF_LOCATION = "/Users/martinstephenson/Desktop"
PDF_NAME = "RA Episode Guide.pdf"

DEFAULT_FONT_BOLD = "Helvetica-Bold"

COVER_IMAGE = "https://is3-ssl.mzstatic.com/image/thumb/Podcasts115/v4/08/8e/9f/088e9f33-0c26-bdf9-a0dc-8e354d06a24f/mza_14163052137543474829.png/313x0w.png"
COVER_TEXT = "The Retro Asylum Podcast".upper()
COVER_SUB_TEXT = "Episode Guide".upper()
COVER_FONT_SIZE = 36
COVER_FONT_COLOUR = colors.black
COVER_IMAGE_WIDTH = 525
COVER_LINK = "http://retroasylum.com/"
COVER_TEXT_Y_CM = 27 * cm
COVER_SUB_TEXT_Y_CM = 2 * cm

TOC_FONT_SIZE = 10
TOC_FONT_COLOUR = colors.black
TOC_TEXT = "Table Of Contents"
TOC_SPACING_DELTA = 0.5

EPISODE_IMAGE_WIDTH = 530
EPISODE_TEXT_Y_CM = 28 * cm
EPISODE_FONT_SIZE = 18
EPISODE_FONT_COLOUR = colors.black

LISTEN_IMAGE = "https://i.imgur.com/gPHLuVM.jpg"
LISTEN_IMAGE_WIDTH = 140
LISTEN_IMAGE_Y = 5
