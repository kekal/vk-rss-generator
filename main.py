import os
import time

from atom_read import parse_atom
from atom_write import AtomGenerator
from parse_html import make_html_obj_from_link, retrieve_links_from_thumbnail_page, analise_photo_page
from sources_import import import_sources

file_names, sources, feed_size, login, password = import_sources('sources.txt')

for j in xrange(0, len(sources)):
    print '\nTrying to parse album ' + sources[j] + '\n'

    if os.path.isfile(file_names[j]):
        feed_parameters_db = parse_atom(file_names[j])
    else:
        feed_parameters_db = {'messages': []}

    feed_parameters_db['main_link'] = sources[j]

    album_page_html_object = make_html_obj_from_link(feed_parameters_db['main_link'])
    if album_page_html_object is None:
        continue

    feed_parameters_db['feed caption'] = album_page_html_object.xpath('//title/text()')[0].split('|')[0].strip()
    links = retrieve_links_from_thumbnail_page(
        album_page_html_object.xpath('//div[@class="photo_row"]'))[:feed_size]

    messages = []
    for i in xrange(0, len(links)):
        mess = analise_photo_page(links[i])
        if next((x for x in feed_parameters_db['messages'] if x.photo_hash == mess.photo_hash), None) is not None:
            # feed_parameters_db['links'].remove(link)
            continue

        # messages.append(mess)
        feed_parameters_db['messages'].insert(i, mess)
        time.sleep(1)

    # messages.extend(feed_parameters_db['messages'])
    # feed_parameters_db['messages'] = messages

    AG = AtomGenerator(feed_parameters_db, file_names[j])
    AG.generate_xml()
