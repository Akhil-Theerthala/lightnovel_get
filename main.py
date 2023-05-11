import os

from Sites.at_get import at_get
from Sites.nf_get import nf_get
from Sites.ww_get import ww_get
from Sites.sky import sky_get
from Sites.nn_get import nn_get
from ebooklib import epub

# Taking the input from the user
Fname = input('What is the name of the novel?')
nov_name = Fname.casefold().replace(' ', '-')
ln_source = input(
    'Where is the novel from? \n ----IF it is Novelfull, then enter "nf" \n ----IF it is WuxiaWorld, then enter "ww" \n ----IF it is Active Translations, then enter "at" \n ').casefold()
if '"' in ln_source:
    ln_source.remove('"')
elif ln_source is None:
    print("Please enter a valid Light Novel source!")

# Some important text:
hdr = ({'User-Agent':
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
			'Accept-Language': 'en-US, en;q=0.5'})

# Create The EPUB File
book = epub.EpubBook()
book.set_language('en')

if ln_source == 'nf':
    nf_get(nov_name, hdr, book)
elif ln_source == 'ww':
    ww_get(nov_name, hdr, book)
elif ln_source == 'at':
    at_get(nov_name, hdr, book)
elif ln_source == 'sky':
    sky_get(nov_name, hdr, book)
elif ln_source == 'nn':
    nn_get(nov_name, hdr, book)

# Add Navigation Files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Defines CSS Style
style = 'p { text-align : left; }'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# Adds CSS File
book.add_item(nav_css)

# Saves Your EPUB File
epub.write_epub('./novels/', book, {})

# Location File Got Saved
print('Saved as', Fname)
