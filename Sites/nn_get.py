from bs4 import BeautifulSoup as bs
import requests as req
from ebooklib import epub
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options

DRIVER_PATH = r'C:\Webdrivers'

options = Options()
options.headless = True
options.add_argument('--window-size=1366,768')

def nn_get(nov_name, hdr, book):
    print('Parsing from  NovelNext initiated!!')
    usr_inp = str('https://novelnext.com/novelnext/'+ nov_name + '#tab-chapters-title')

    # Running the browser
    driver = webdriver.Edge(executable_path=DRIVER_PATH + r'\msedgedriver.exe', options=options)
    driver.get(usr_inp)

    time.sleep(10)

    # The start of the main code:
    response = driver.page_source
    soup = bs(response, 'html.parser')
    print("The soup is boiled.")
    # Getting the links from the url provided:
    link_src = soup.find_all('ul', class_='list-chapter')
    ch_name = []
    links = []
    for u in link_src:
        link_list_src = u.find_all('li')
        for l in link_list_src:
            ch_name.append(l.text)
            links.append(l.a.attrs['href'])
    print(links)
    # Generating the book:
    for k in range(len(links)):
        ch_src = req.get(links[k]).text
        s = bs(ch_src, 'lxml')
        chap_cont = s.find('div', class_='chr-c')

        # Creating a chapter
        c2 = epub.EpubHtml(title=ch_name[k], file_name='Chapter ' + str(k) + '.xhtml', lang='hr')
        c2.content = chap_cont.encode("utf-8")
        book.add_item(c2)

        # Add to table of contents
        book.toc.append(c2)
        # Add to book ordering
        book.spine.append(c2)
        print("Added", ch_name[k])
