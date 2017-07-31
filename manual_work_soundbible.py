from credentials import host, db_name, db_password, db_user
from webscrapper_class_soundbible import get_meta_data as MD
from webscrapper_mysql_libraries_soundbible import *
from pprint import pprint as p


db = connection(host, db_user, db_password, db_name)


error_list = []


auto_mode = raw_input('auto?')

if auto_mode == 'y':
    meta_data = MD(error_list[0])

    insert_into_table(db, meta_data)

else:

    title = raw_input("Title:")
    download = raw_input("Download:")
    description = raw_input("Description:")
    license = raw_input("License:")
    filesize = raw_input("Filesize:")
    tags = raw_input("Tags")

    meta_data = {}
    meta_data['title'] = title
    meta_data['download'] = download
    meta_data['description'] = description
    meta_data['license'] = license
    meta_data['filesize'] = filesize
    meta_data['tags'] = tags

    insert_into_table(db, meta_data)


destroy_connection(db)