import urllib2
import MySQLdb
import urlparse
import mechanize as mech
import cookielib
from bs4 import BeautifulSoup as soup


cj = 0

def get_download_links(db, array):
    try:
        cr = db.cursor()
        cr.execute("SELECT download FROM freesound")
    except MySQLdb.Error, e:
        print e
        return e
    for dl in cr.fetchall():
        array.append(dl)

def get_file_id(link):
    link_id = str(link).split('download/')[-1]
    print(link_id)
    return link_id

def download_file(link, link_id):
    name = str(link_id).split('.')[0]
    type = str(link_id).split('.')[-1]

    br = mech.Browser()
    br.set_cookiejar(cj)
    br.retrieve(link, 'music_files/freesound/' + name + '.' + type)



def login_error_handler(error_html):
    error_soup = soup(error_html, 'html.parser')
    error_msg = error_soup.find('ul', {'class':'errorlist nonfield'})

    if error_msg != None:
        return error_msg.li.decode_contents(formatter='html')
    else:
        return 'Logged In'

def login_handler(username, password):
    br = mech.Browser()

    global cj

    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)



    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_debug_redirects(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mech._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Chrome')]

    br.open('https://www.freesound.org/home/login/?next=/home/login/')

    br.select_form(nr=1)

    br.select_form(nr=1)

    br.form['username'] = username
    br.form['password'] = password

    response = br.submit()
    print(login_error_handler(response))