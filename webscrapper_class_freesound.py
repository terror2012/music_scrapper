import mechanize as mech
from bs4 import BeautifulSoup as soup
import cookielib
from urllib import urlopen as uReq
import urllib
import re
import urlparse


def get_page_number(url):
    pageClient = uReq(url)
    page_html = pageClient.read()
    pageClient.close()
    page_soup = soup(page_html, 'html.parser')
    pages = page_soup.find('div', {'class':'search_paginator'}).ul.find('li', {'class' : 'last-page'}).a.decode_contents(formatter='html')

    return pages

def get_page_content(url, error_link_array):
    try:
        contentClient = uReq(url)
        content_html = contentClient.read()
        contentClient.close()

        print(url + ' -> getting content from here')

        if content_html == None:
            error_link_array.append(url)
            return None

        return content_html
    except:
        print(url + '   ->error Link!')
        get_page_content(iriToUri(url), error_link_array)


def sample_more_search_result(url):

    try:
        sampleClient = uReq(url)
        sample_html = sampleClient.read()
        sampleClient.close()

        sample_soup = soup(sample_html, 'html.parser')

        sample_result = sample_soup.find('div', {'id': 'wrapper'}).find('div', {'id': 'container'}).find('div', {
            'id': 'content_full'}).find_all('div', {'class': 'sample_more_search_results'})

        samples = []

        for sample in sample_result:
            if sample != None:
                samples.append('https://www.freesound.org' + sample.a['href'])

        return samples
    except Exception, e:
        sample_more_search_result(iriToUri(url))
        print (e)

def get_sound_link(page):
    try:
        sound_soup = soup(page, 'html.parser')

        page_content_full = sound_soup.find('div', {'id': 'wrapper'}).find('div', {'id': 'container'}).find('div', {
            'id': 'content_full'}).find_all('div', {'class': 'sample_player_small'})

        links = []

        for titles in page_content_full:
            a_link = titles.find('div', {'class': 'sample_player'}).find('div', {'class': 'sound_title'}).find('div', {
                'class': 'sound_filename'})
            link = a_link.a['href']
            print('https://www.freesound.org' + link + ' -> getting_sound_link')
            links.append('https://www.freesound.org' + link)

        return links
    except Exception, e:
        print(e)


def sample_page_number(url):

    try:
        pageClient = uReq(url)
        page_html = pageClient.read()
        pageClient.close()
        page_soup = soup(page_html, 'html.parser')
        if page_soup.find('div', {'class': 'search_paginator'}) and len(
                page_soup.find('div', {'class': 'search_paginator'}).find_all('li', {'class': 'other-page'})) > 1:
            pages = page_soup.find('div', {'class': 'search_paginator'}).ul.find_all('li', {'class': 'other-page'})[
                -1].a.decode_contents(formatter='html')
            return pages
        else:
            return 1
    except:
        sample_page_number(iriToUri(url))


def get_file_meta(url):
    try:
        sound_array = {}
        soundClient = uReq(url)
        sound_html = soundClient.read()
        soundClient.close()
        tags = []
        sound_soup = soup(sound_html, 'html.parser')
        sound_name = sound_soup.find('div', {'id': 'single_sample_header'}).getText()
        sound_description = sound_soup.find('div', {'id': 'sound_description'}).p.getText()
        sound_tag = sound_soup.find('ul', {'class': 'tags'}).find_all('li')
        for sound in sound_tag:
            tags.append(sound.getText())

        sound_tags = ','.join(tags)
        sound_download = sound_soup.find('div', {'id': 'download'}).a['href']
        sound_license = sound_soup.find('div', {'id': 'sound_license'}).a.getText()
        sound_type = \
        sound_soup.find('dl', {'id': 'sound_information_box'}).find_all(
            'dd')[0].getText()
        sound_duration = \
        sound_soup.find('dl', {'id': 'sound_information_box'}).find_all(
            'dd')[1].getText()
        sound_filesize = \
        sound_soup.find('dl', {'id': 'sound_information_box'}).find_all(
            'dd')[2].getText()
        sound_bitrate = \
        sound_soup.find('dl', {'id': 'sound_information_box'}).find_all(
            'dd')[3].getText()
        sound_channels = \
        sound_soup.find('dl', {'id': 'sound_information_box'}).find_all(
            'dd')[4].getText()
        sound_array['name'] = sound_name.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['description'] = sound_description.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['tags'] = sound_tags.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['license'] = sound_license.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['type'] = sound_type.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['duration'] = sound_duration.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['filesize'] = sound_filesize.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['bitrate'] = sound_bitrate.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['channels'] = sound_channels.encode('utf-8').replace("'", "").replace("\n", "")
        sound_array['download'] = 'https://www.freesound.org' + sound_download.encode('utf-8')

        return sound_array
    except Exception, e:
        print(e)
        get_file_meta(iriToUri(url))


def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )
