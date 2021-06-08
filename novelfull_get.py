	#Issue-4: The 'About-Novel' page
#Issue-5: Proper Introduction.
#Issue-7: Should optimise the code and make it look neat.


import os
from bs4 import BeautifulSoup as bs
import requests as req
from ebooklib import epub

# Create The EPUB File
book = epub.EpubBook()
book.set_language('en')

# Novelfull link Dont Change this!!!!
nf = 'https://novelfull.com'   

#Geeting the content and passing it to BS4:
usr_inp = input('Enter the novel link here:')
ch_num = int(input('How many chapters are there in the novel?'))
num_pages = int(ch_num / 50) +1

#The start of the main code:
for i in range(1,num_pages+1):
	if i==1:
		src = req.get(usr_inp).text
	elif i >= 2:
		src = req.get(usr_inp+'?page='+str(i)+'&per-page=50').text    		 ##
	soup = bs(src, 'lxml')


	#Getting the links from the url provided:
	link_src = soup.find_all('ul', class_ ='list-chapter')
	ch_name=[]
	links = []
	for u in link_src:
		link_list_src = u.find_all('li')
		for l in link_list_src:
			link_suff = l.a.attrs['href']
			ch_name.append(l.text)
			links.append(nf + link_suff)


	#Generating the book:
	for k in range(len(links)):
		ch_src=req.get(links[k]).text
		s= bs(ch_src, 'lxml')
		chap_cont = s.find('div' , class_='chapter-c')	

		 # Creating a chapter
		c2 = epub.EpubHtml(title=ch_name[k], file_name=ch_name[k]+'.xhtml', lang='hr')
		c2.content = chap_cont.encode("utf-8")
		book.add_item(c2)

		# Add to table of contents
		book.toc.append(c2)
		# Add to book ordering
		book.spine.append(c2)			          

		print("Added",ch_name[k])
 
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

#font-family:Roboto, Roboto 400, serif; 