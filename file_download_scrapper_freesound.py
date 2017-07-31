from webscrapper_mysql_libraries_freesound import connection, destroy_connection
from credentials import host, db_user, db_password, db_name
from file_download_scrapper_class_freesound import get_download_links as DL
from file_download_scrapper_class_freesound import get_file_id as ID
from file_download_scrapper_class_freesound import download_file as DLD
import time
from pprint import pprint as p

db = connection(host, db_user, db_password, db_name)

download_links = []

DL(db, download_links)

for links in download_links:
    link = ''.join(map(str, links))
    print(link)
    link_id = ID(link)
    DLD(link, link_id)

destroy_connection(db)