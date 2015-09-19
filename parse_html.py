from pydoc import html


def make_html_obj_from_link(link, mode='desktop'):
    import urlparse
    import requests
    from lxml.html import make_links_absolute

    if mode == 'mobile':
        try:
            response = requests.get(link, headers={'User-Agent': 'blahblah iPhone'})
        except requests.exceptions.ConnectionError:
            print 'link ' + link + ' unreachable'
            return
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse.urlparse(response.url))[:-1]
        body = make_links_absolute(response.content, domain)
    else:
        try:
            response = requests.get(link)
        except requests.exceptions.ConnectionError:
            print 'link ' + link + ' unreachable'
            return
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse.urlparse(response.url))[:-1]
        body = make_links_absolute(response.content.decode('cp1251'), domain)

    from lxml import html
    parsed_body = html.fromstring(body)
    return parsed_body


def analise_photo_page(link):
    from lxml.etree import tostring

    link = link.replace('http://vk', 'http://m.vk')

    print 'parsing page ' + link

    photo_page_object = make_html_obj_from_link(link, 'mobile')

    author = photo_page_object.xpath('//div[@class="mv_details"]/dl[2]/dd/a/text()')
    if not author:
        author = ''
    else:
        author = author[0]

    author_link = photo_page_object.xpath('//div[@class="mv_details"]/dl[2]/dd/a/@href')
    if not author_link:
        author_link = ''
    else:
        author_link = author_link[0]

    descript = photo_page_object.xpath('//div[@class="mv_description"]/node()')

    title = []

    for desc in descript:
        if not isinstance(desc, (str, basestring)):
            title.append(tostring(desc))
        else:
            title.append(desc)
    title = ' '.join(title)
    title = html.escape(title)

    image = photo_page_object.xpath('//li/a[@target="_blank"]/@href')
    if not image:
        print link, ' has not been parsed correctly'
        print image, '\n'
        with open(link.split('/')[-1] + '.html', 'w') as source:
            source.write(tostring(photo_page_object))
        image = ''
    else:
        image = image[0]
        photo_hash = image.split('.')[-2].split('/')[-1]

    from PostParamsContainer import PostParamsContainer
    return PostParamsContainer(link, title, author, author_link, image, photo_hash=photo_hash)


def retrieve_links_from_thumbnail_page(blocks):
    urls = []
    for block in blocks:
        l = block.xpath('./a/@href')
        if len(l) == 0:
            print 'wrong block ', block.xpath('./text()')
            continue
        urls.append(l[0].replace('?all=1', ''))

    return urls
