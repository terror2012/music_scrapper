from credentials import host, db_name, db_password, db_user
from webscrapper_class_soundbible import get_max_page as MP
from webscrapper_class_soundbible import get_content_link as CL
from webscrapper_class_soundbible import get_meta_data as MD
from webscrapper_mysql_libraries_soundbible import *
from pprint import pprint as p

pages = int(MP('http://soundbible.com/free-sound-effects-1.html'))

second_pages = int(MP('http://soundbible.com/royalty-free-sounds-1.html'))

db = connection(host, db_user, db_password, db_name)

if check_table_if_exists(db) == 1146:
    create_table(db)
else:
    print('Table already exists!')

pages_links = []

curr_page = 1

very_serious_error_links = []

sound_download_links = []

error_urls = []

curr_second_page = 1

while curr_page <= pages:
    CL('http://soundbible.com/free-sound-effects-' + str(curr_page) + '.html', pages_links)
    curr_page += 1

while curr_second_page <= second_pages:
    CL('http://soundbible.com/royalty-free-sounds-' + str(curr_second_page) + '.html', pages_links)
    curr_second_page += 1

all_links = set(pages_links)

print(len(all_links))

for pages in all_links:
    try:
        meta_data = MD(pages)
        insert_into_table(db, meta_data)
    except:
        error_urls.append(pages)
        continue

for page in error_urls:
    try:
        meta_data = MD(pages)
        insert_into_table(db, meta_data)
    except:
        very_serious_error_links.append(pages)
        continue

print(very_serious_error_links)

destroy_connection(db)