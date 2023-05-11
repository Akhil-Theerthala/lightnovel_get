from bs4 import BeautifulSoup as bs
import requests as req
from ebooklib import epub


def sky_get(nov_name, hdr, book):
    usr_inp = str('https://skydemonorder.com/projects/' + nov_name)

    try:
        #The start of the main code:
        src = req.get(usr_inp, headers= hdr).text
        soup = bs(src, 'lxml')

        #Getting the links from the url provided:
        link_src = soup.find_all('div', class_ ='flex items-center py-4 pr-6')
        ch_name=[]
        links = []
        for u in link_src:
            link_list_src = u.find_all('a')
            for a in link_list_src:
                link_suff = a.attrs['href']
                ch_name.append(a.text.strip())
                links.append(link_suff)
        
        ch_name = ch_name[10:]
        links = links[10:]

        ch_name = ch_name[::-1]
        links = links[::-1]

	
    finally:
        #Generating the book:
        for k in range(len(links)):
            HEADERS = ({'User-Agent':
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
			'Accept-Language': 'en-US, en;q=0.5'})

            ch_src=req.get(links[k], headers=HEADERS)
            s= bs(ch_src.content, 'html.parser')
            chap_cont = s.find('div' , class_="prose max-w-none pb-10 font-medium text-primary-600")	
            # print(chap_cont)
            # Creating a chapter
            c2 = epub.EpubHtml(title=ch_name[k], file_name=ch_name[k] +'.xhtml', lang='hr')
            c2.content = chap_cont.encode("utf-8")
            book.add_item(c2)

            # Add to table of contents
            book.toc.append(c2)
            # Add to book ordering
            book.spine.append(c2)			          

            print("Added",ch_name[k])

                