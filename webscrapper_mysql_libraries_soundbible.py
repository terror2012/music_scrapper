import MySQLdb

def connection(host, user, passwd, db):
    db = MySQLdb.connect(host = host, user = user, passwd = passwd, db = db)
    print('Connection established')
    return db


def create_table(db):
    try:
        cr = db.cursor()
        cr.execute('CREATE TABLE sound_bible (title VARCHAR(50), download VARCHAR(50), description LONGTEXT, license VARCHAR(50), filesize VARCHAR(50), tags LONGTEXT)')
        print 'success'
    except MySQLdb.Error, e:
        print e

def check_table_if_exists(db):
    try:
        cr = db.cursor()
        cr.execute('SELECT 1 FROM sound_bible LIMIT 1;')
        print cr.fetchall()
    except MySQLdb.Error, e:
        print e[0]
        return e[0]

def check_for_duplicated(db, download_link, title):
    cr = db.cursor()
    cr.execute("""SELECT * FROM sound_bible WHERE download = '{0}' """.format(download_link))
    if cr.rowcount != 0:
        print('{0} already exists'.format(title))
        return True
    else:
        print('False')
        return False

def insert_into_table(db, array):
    title = array['title']
    download = array['download']
    description = array['description']
    license = array['license']
    filesize = array['filesize']
    tags = array['tags']
    if check_for_duplicated(db, download, title) == False:
        try:
            cr = db.cursor()
            cr.execute("INSERT INTO sound_bible VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(title, download, description, license, filesize, tags))
            db.commit()
            print 'Successful added {0} to database'.format(title)
        except MySQLdb.Error, e:
            print e
            return e

def destroy_connection(db):
    db.close()
    print('Connection closed')
