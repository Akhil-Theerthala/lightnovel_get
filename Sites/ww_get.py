from bs4 import BeautifulSoup as bs
import requests as req
from ebooklib import epub


def ww_get(nov_name,hdr,book):
	#Do not change this!!
	ww = 'https://wuxiaworld.com'
	print('\n NOTE!!!!\n The completed novels cannot be scraped...\n')

	usr_inp = ww+ '/novel/'+ nov_name

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
 