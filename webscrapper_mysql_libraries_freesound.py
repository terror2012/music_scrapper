import MySQLdb

def connection(host, user, passwd, db):
    db = MySQLdb.connect(host = host, user = user, passwd = passwd, db = db)
    print('Connection established')
    return db


def create_table(db):
    try:
        cr = db.cursor()
        cr.execute('CREATE TABLE freesound (name VARCHAR(200), description LONGTEXT, tags LONGTEXT, license VARCHAR(200), type VARCHAR(200), duration VARCHAR(200), filesize VARCHAR(200), bitrate VARCHAR(200), channels VARCHAR(200), download VARCHAR(1000))')
        print 'success'
    except MySQLdb.Error, e:
        print e

def check_table_if_exists(db):
    try:
        cr = db.cursor()
        cr.execute('SELECT 1 FROM freesound LIMIT 1;')
        print cr.fetchall()
    except MySQLdb.Error, e:
        print e[0]
        return e[0]

def check_for_duplicated(db, download_link, title):
    cr = db.cursor()
    cr.execute("""SELECT * FROM freesound WHERE download = '{0}' """.format(download_link))
    if cr.rowcount != 0:
        print('{0} already exists'.format(title))
        return True
    else:
        print('False')
        return False

def insert_into_table(db, array):
    name = array['name']
    description = array['description']
    tags = array['tags']
    license = array['license']
    type = array['type']
    duration = array['duration']
    filesize = array['filesize']
    bitrate = array['bitrate']
    channels = array['channels']
    download = array['download']
    if check_for_duplicated(db, download, name) == False:
        try:
            cr = db.cursor()
            cr.execute("""INSERT INTO freesound VALUES ('{0}','{1}','{2}','{3}','{4}','{5}', '{6}', '{7}', '{8}', '{9}')""".format(name, description, tags, license, type, duration, filesize, bitrate, channels, download))
            db.commit()
            print 'Successful added {0} to database'.format(name)
        except MySQLdb.Error, e:
            print e
            return e

def destroy_connection(db):
    db.close()
    print('Connection closed')
