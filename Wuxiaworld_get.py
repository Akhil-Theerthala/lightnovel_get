import os
from bs4 import BeautifulSoup as bs
import requests as req
from ebooklib import epub

# Create The EPUB File
book = epub.EpubBook()
book.set_language('en')

#Do not change this!!
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
ww = 'https://wuxiaworld.com'
print('\n NOTE!!!!\n The completed novels cannot be scraped...\n')

#novel link

nov_name = input('Enter the name of the novel you want to scrape').casefold().replace(' ','-')
usr_inp = ww+ '/novel/'+ nov_name
print(usr_inp)
#Passing to BS4
src = req.get(usr_inp, headers = hdr)
soup = bs(src.text, 'lxml')



#getting the links of all chapters:
links = []
ch_name = []	
li =  soup.find_all('li', class_="chapter-item")
for l in li:
    href = l.a.attrs["href"]
    ch_name.append(l.text.strip())
    link = ww + href
    links.append(link)

print('Number of available chapters: {} \n'.format(len(links)))

#Generating the book:
for i in range(len(links)):
	ch_src = req.get(links[i], headers = hdr)
	ch_title = ch_name[i]
	s= bs(ch_src.text , 'lxml')
	chap_cont = s.find('div' , class_='fr-view')
	

	# Creating a chapter
	c2 = epub.EpubHtml(title=ch_name[i], file_name='Chapter '+ str(i) +'.xhtml', lang='hr')
	c2.content = chap_cont.encode("utf-8")
	book.add_item(c2)

	# Add to table of contents
	book.toc.append(c2)
	# Add to book ordering
	book.spine.append(c2)			          
 
	print("Added",ch_name[i])
 
# Add Navigation Files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Defines CSS Style
style = 'p { text-align : left; }'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# Adds CSS File
book.add_item(nav_css)

#Saving the file as an epub document
pathToLocation = input('Enter the path where you would like to save the Ebook:\n (example:/home/username/Desktop/) \n')
Fname = input('What would you like to name it as?') + '.epub'
saveLocation = pathToLocation + Fname


print("Saving . . . . . . ")

# Saves Your EPUB File
epub.write_epub(saveLocation, book, {})

# Location File Got Saved
print('Saved at', pathToLocation, 'as' , Fname)
