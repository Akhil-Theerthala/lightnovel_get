from Sites.at_get import at_get
from Sites.nf_get import nf_get
from Sites.ww_get import ww_get
from ebooklib import epub

# Taking the input from the user
nov_name = input('What is the name of the novel?').casefold().replace(' ','-')
ln_source = input('Where is the novel from? \n ----IF it is Novelfull, then enter "nf" \n ----IF it is WuxiaWorld, then enter "ww" \n ----IF it is Active Translations, then enter "at" \n ').casefold()
if '"' in ln_source:
    ln_source.remove('"')


#Some important text:
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

# Create The EPUB File
book = epub.EpubBook()
book.set_language('en')

if ln_source == 'nf':
    nf_get(nov_name,hdr,book)    
elif ln_source == 'ww':
    ww_get(nov_name,hdr,book)
elif ln_source == 'at':
    at_get(nov_name,hdr,book)



# Add Navigation Files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Defines CSS Style
style = 'p { text-align : left; }'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# Adds CSS File
book.add_item(nav_css)

#Saving the file as an epub document
pathToLocation = input('Enter the path where you would like to save the Ebook:\n (example:/home/username/Desktop/)')
Fname = input('What would you like to name it as?') + '.epub'
saveLocation = pathToLocation + Fname


print("Saving . . . . . . ")

# Saves Your EPUB File
epub.write_epub(saveLocation, book, {})

# Location File Got Saved
print('Saved at', pathToLocation, 'as' , Fname)