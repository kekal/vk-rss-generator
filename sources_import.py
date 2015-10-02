import os


def import_sources(path):
    path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.isfile(path):
        raise IOError('file \"' + path + '\" does NOT exist.')

    feed_size = 20
    login = password = ''
    file_names = []
    links = []

    with open(path) as sources:
        sources = sources.readlines()

    for source in sources:
        if 'http' in source:
            file_names.append(source.split('/')[-1].strip() + '.atom')
            links.append(source.strip())
            continue

        if 'name' in source:
            login = ':'.join(source.split(':')[1:]).strip()
            continue

        if 'password' in source:
            password = ':'.join(source.split(':')[1:]).strip()
            continue

        if 'feed size' in source:
            temp = ':'.join(source.split(':')[1:]).strip()
            try:
                feed_size = int(temp)
            except ValueError:
                continue

    return file_names, links, feed_size, login, password
