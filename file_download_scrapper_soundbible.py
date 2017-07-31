from webscrapper_mysql_libraries_soundbible import connection, destroy_connection
from credentials import host, db_user, db_password, db_name
from file_download_scrapper_class_soundbible import get_download_links as DL
from file_download_scrapper_class_soundbible import get_file_id as ID
from file_download_scrapper_class_soundbible import download_file as DLD
from file_download_scrapper_class_soundbible import get_file_type as FT
from pprint import pprint as p

db = connection(host, db_user, db_password, db_name)

download_links = []

DL(db, download_links)

for links in download_links:
    link = 'http://' + ''.join(map(str, links))
    print(link)
    DLD(link, ID(link), FT(link))

destroy_connection(db)