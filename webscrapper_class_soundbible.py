import mechanize as mech
from bs4 import BeautifulSoup as soup
import cookielib
from urllib import urlopen as uReq
from pprint import pprint as p


def get_soup_content(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'html.parser')

    return page_soup

def get_max_page(url):
    page_soup = get_soup_content(url)

    pages = page_soup.find('div', {'id':'wrap'}).find('div', {'id':'content'}).table.find_all('tr')[0].find_all('td')[1].find_all('a')[-1].getText()
    return pages


def get_content_link(url, array):
    page_soup = get_soup_content(url)

    links_soup = page_soup.find('div', {'id':'wrap'}).find('div', {'id':'content'}).table.find_all('tr', {'class':'row-b'})

    del links_soup[0]
    del links_soup[-1]

    for link in links_soup:
        url ='http://soundbible.com/' + str(link.td.a['href'])
        print(url)
        array.append(url)

def get_meta_data(url):
        page_soup = get_soup_content(url)
        page_content = page_soup.find('div', {'id': 'wrap'}).find('div', {'id': 'content'}).find('div', {'id': 'main'})
        meta_data = {}
        sound_title = page_content.find_all('h2')[0].getText()

        print(sound_title)

        page_soup.html.decompose()
        sound_download = 'soundbible.com/' + str(page_soup.find_all('a')[1]['href'])
        sound_description = page_soup.find('div', {'typeof': 'v:Review-aggregate'}).find('span', {
            'property': 'v:summary'}).getText()
        sound_data_text = page_soup.find('div', {'typeof': 'v:Review-aggregate'}).getText()
        sound_license = 'License: ' + str(sound_data_text.split('License:')[1].split('|')[0][:-1])
        sound_filesize = 'File Size: ' + str(sound_data_text.split('File Size:')[1].split('|')[0][:-1])
        sound_tags_html = page_soup.find_all('div')[6].p.find_all('a')
        sound_tag = []

        for a in sound_tags_html:
            sound_tag.append(a.getText())

        sound_tags = ','.join(sound_tag)

        meta_data['title'] = sound_title.encode('utf-8')
        meta_data['download'] = sound_download.encode('utf-8')
        meta_data['description'] = sound_description.encode('utf-8')
        meta_data['license'] = sound_license.encode('utf-8')
        meta_data['filesize'] = sound_filesize.encode('utf-8')
        meta_data['tags'] = sound_tags.encode('utf-8')

        print(sound_download)
        return meta_data



