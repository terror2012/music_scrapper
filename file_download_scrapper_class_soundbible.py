import urllib2
import MySQLdb
import urlparse

def get_download_links(db, array):
    try:
        cr = db.cursor()
        cr.execute("SELECT download FROM sound_bible")
    except MySQLdb.Error, e:
        print e
        return e
    for dl in cr.fetchall():
        array.append(dl)

def get_file_id(link):
    pUrl = urlparse.urlparse(link)
    link_id = urlparse.parse_qs(pUrl.query)['id'][0]
    print(link_id)
    return link_id

def get_file_type(link):
    pUrl = urlparse.urlparse(link)
    link_type = urlparse.parse_qs(pUrl.query)['type'][0]
    print(link_type)
    return link_type


def download_file(link, link_id, link_type):
    try:
        sound = urllib2.urlopen(link)
        with open('music_files/sound_bible/{0}.{1}'.format(link_id, link_type), 'wb') as output:
            output.write(sound.read())
    except Exception, e:
        print e
        return e