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

    author_name = photo_page_object.xpath('//div[@class="mv_details"]/dl[2]/dd/a/text()')
    author_name = '' if author_name else author_name[0]

    author_link = photo_page_object.xpath('//div[@class="mv_details"]/dl[2]/dd/a/@href')
    author_link = '' if author_link else author_link[0]

    # title = photo_page_object.xpath('//div[@class="mv_description"]/text()')
    # if title:
    #     temp = ''
    #     for tit in title:
    #         temp += tit
    #     title = temp
    # else:
    #     title = ''

    description = photo_page_object.xpath('//div[@class="mv_description"]/node()')
    title = ''
    if description:
        content = []
        for desc in description:
            if not isinstance(desc, (str, basestring, unicode)):
                content.append(tostring(desc))
            else:
                content.append(desc)
                title += desc
        content = ' '.join(content)
        content = html.escape(content)
    else:
        content = html.escape(photo_page_object.xpath('//div[@class="pv_summary"]/text()')[0])
        title = content


    image_link = photo_page_object.xpath('//li/a[@target="_blank"]/@href')
    if not image_link:
        print link, ' has not been parsed correctly'
        print image_link, '\n'
        with open(link.split('/')[-1] + 'NotCorrectlyParsedPage.html', 'w') as source:
            source.write(tostring(photo_page_object))
        image_link = ''
        photo_hash = ''
    else:
        image_link = image_link[0]
        photo_hash = image_link.split('.')[-2].split('/')[-1]

    from PostParamsContainer import PostParamsContainer
    # page_link='', description='', author_name='', author_link='', image_link='', time='', photo_hash='', content=''
    return PostParamsContainer(link, title, author_name, author_link, image_link, photo_hash=photo_hash, content=content)


def retrieve_links_from_thumbnail_page(blocks):
    urls = []
    for block in blocks:
        l = block.xpath('./a/@href')
        if len(l) == 0:
            print 'wrong block ', block.xpath('./text()')
            continue
        urls.append(l[0].replace('?all=1', ''))

    return urls
