from webscrapper_class_freesound import get_page_number as PG
from webscrapper_class_freesound import get_page_content as GC
from credentials import USERNAME, PASSWORD, host, db_user, db_password, db_name
from webscrapper_class_freesound import sample_more_search_result as SR
from webscrapper_class_freesound import get_sound_link as SL
from pprint import pprint as p
from webscrapper_class_freesound import sample_page_number as SM
from webscrapper_class_freesound import get_file_meta as FM
from webscrapper_mysql_libraries_freesound import *

db = connection(host, db_user, db_password, db_name)

if check_table_if_exists(db) == 1146:
    create_table(db)
else:
    print('Table already exists!')

page_nr = PG('https://www.freesound.org/search/?q=&page=1#sound')

page_nr = int(page_nr)

print(page_nr)

curr_page = input("Page number to start!")
curr_page = int(curr_page)

error_link_array = []

def mainLoop(curr_page):

    while curr_page <= page_nr:

        try:
            print(str(curr_page) + ' -> current page')

            page_content = GC('https://www.freesound.org/search/?q=&page=' + str(curr_page) + '#sound',
                              error_link_array)

            sample_links = SR('https://www.freesound.org/search/?q=&page=' + str(curr_page) + '#sound')

            sample_content = []

            sound_array = []

            for sam in sample_links:
                if SM(sam) is not None:
                    page_size = int(SM(sam))
                else:
                    page_size = 1

                print(str(page_size) + ' -> number of pages')

                curr_sample_page = 1

                while curr_sample_page <= page_size:
                    sample_content.append(
                        GC(sam + '&advanced=&page=' + str(curr_sample_page) + '#sound', error_link_array))
                    curr_sample_page += 1

            if page_content is not None:
                sound_array.append(SL(page_content))

            for sound in sample_content:
                if sound is not None:
                    sound_array.append(SL(sound))

            for ss in sound_array:
                if ss is not None:
                    for sounds in ss:
                        meta_data = FM(sounds)
                        insert_into_table(db, meta_data)
        except:
            print(curr_page)
            continue

        curr_page += 1

mainLoop(curr_page)

destroy_connection(db)