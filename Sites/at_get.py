from bs4 import BeautifulSoup as bs
import requests as req
from ebooklib import epub



def at_get(nov_name,hdr,book):

	usr_inp = 'https://a-t.nu/novel/'+ nov_name +'/'															#inp
	usr_inp_fchap = int(input('From which chapter does the novel begin in this site? \n (VIP as soon as you log in begins at chapter 28) \n Enter Here:'))
	usr_inp_lchap = int(input('Enter the last chapter which you want to scrape:'))																							#inp

	#getting the links of all chapters:
	links = []
	for i in range(usr_inp_fchap, usr_inp_lchap+1):
		links.append( usr_inp+ nov_name +'/'+'chapter-'+str(i))

	print('Links Obtained')

	
	for i in range(len(links)):
		ch_src = req.get(links[i], headers = hdr)
		s= bs(ch_src.text , 'lxml')
		chap_cont = s.find('div' , class_="text-left")
	

		# Creating a chapter
		c2 = epub.EpubHtml(title='Chapter '+ str(usr_inp_fchap+i) , file_name='Chapter '+ str(usr_inp_fchap+i) +'.xhtml', lang='hr')
		c2.content = chap_cont.encode("utf-8")
		book.add_item(c2)

		# Add to table of contents
		book.toc.append(c2)
		# Add to book ordering
		book.spine.append(c2)			          
 
		print("Added Chapter ",usr_inp_fchap+i)
 
