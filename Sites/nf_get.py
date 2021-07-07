from bs4 import BeautifulSoup as bs
import requests as req
from ebooklib import epub


def nf_get(nov_name, hdr, book, t=0):
	usr_inp = str('https://novelfull.com' + '/' + nov_name + '.html')
	try:
		temp_src =  req.get(usr_inp, headers = hdr)
		s1 = bs(temp_src.text, 'lxml')
		lastpage_get = s1.find('li', class_='last').a.attrs['href'].split('?')[-1].split('&')[0].split('=')[-1]
		num_pages= int(lastpage_get)
	except:
		print('The novel is either not available at Novelfull or the name entered is incorrect')
		quit()

	#The start of the main code:
	for i in range(1,num_pages+1):
		src = req.get(usr_inp+'?page='+str(i)+'&per-page=50', headers= hdr).text
		t+=50
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
				links.append('https://novelfull.com' + link_suff)


		#Generating the book:
		for k in range(len(links)):
			ch_src=req.get(links[k]).text
			s= bs(ch_src, 'lxml')
			chap_cont = s.find('div' , class_='chapter-c')	

			 # Creating a chapter
			c2 = epub.EpubHtml(title=ch_name[k], file_name='Chapter '+ str(k+t) +'.xhtml', lang='hr')
			c2.content = chap_cont.encode("utf-8")
			book.add_item(c2)

			# Add to table of contents
			book.toc.append(c2)
			# Add to book ordering
			book.spine.append(c2)			          
	
			print("Added",ch_name[k])