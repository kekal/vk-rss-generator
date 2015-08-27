from types import NoneType
from lxml import html
from lxml.etree import tostring
from lxml.html import make_links_absolute
import requests
import time

from MessageParams import MessageParams


def make_html_obj_from(link, mode='desktop'):
    import urlparse

    if mode == 'mobile':
        response = requests.get(link, headers={'User-Agent': 'blahblah iPhone'})
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse.urlparse(response.url))[:-1]
        body = make_links_absolute(response.content, domain)
    else:
        response = requests.get(link)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse.urlparse(response.url))[:-1]
        body = make_links_absolute(response.content.decode('cp1251'), domain)

    # print response.url
    parsed_body = html.fromstring(body)
    return parsed_body


def parse_image_blocks(blocks):
    urls = []
    for block in blocks:
        l = block.xpath('./a/@href')
        if len(l) == 0:
            print 'wrong block ', block.xpath('./text()')
            continue
        urls.append(l[0].replace('?all=1', ''))

    return urls


def parse_foto_page(link):
    link = link.replace('http://vk', 'http://m.vk')
    print link
    second_level_html = make_html_obj_from(link, 'mobile')

    author = second_level_html.xpath('//div[@class="mv_details"]/dl[2]/dd/a/text()')
    if not author:
        author = ''
    else:
        author = author[0]

    author_link = second_level_html.xpath('//div[@class="mv_details"]/dl[2]/dd/a/@href')
    if not author_link:
        author_link = ''
    else:
        author_link = author_link[0]

    descript = second_level_html.xpath('//div[@class="mv_description"]/node()')

    title = []
    for desc in descript:
        if isinstance(desc, NoneType):
            params_dict['post_titles'].append('No description')
        elif not isinstance(desc, (str, basestring)):
            title.append(tostring(desc))
        else:
            title.append(desc)
    title = '\n'.join(title)

    image = second_level_html.xpath('//li/a[@target="_blank"]/@href')
    if not image:
        print link, ' has not been parsed correctly'
        print image, '\n'
        with open(link.split('/')[-1] + '.html', 'w') as sourse:
            sourse.write(tostring(second_level_html))
        image = ''
    else:
        image = image[0]

    return MessageParams(link, title, author, author_link, image)


def generate_xml(title, messages, path):
    from datetime import datetime

    now = datetime.now()

    output = '<?xml version="1.0" encoding="UTF-8"?>\n'
    output += '  <feed xml:lang="en-US" xmlns="http://www.w3.org/2005/Atom">\n'
    output += '    <id>tag:' + main_link + ':/post/atom</id>\n'
    output += '    <link rel="alternate" type="text/html" href="' + main_link + '"/>\n'
    output += '    <link rel="self" type="application/atom+xml" href=""/>\n'
    output += '    <title>' + title + '</title>\n'
    output += '    <updated>' + now.isoformat() + '</updated>\n'

    for i in xrange(len(messages)):
        output += '    <entry>\n'
        output += '      <id>tag:' + main_link + ',2005:Post/' + messages[i].image_link.split('/')[-1].split('.')[-2] + '</id>\n'
        output += '      <published>' + now.isoformat() + '</published>\n'
        output += '      <updated>' + now.isoformat() + '</updated>\n'
        output += '      <link rel="alternate" type="text/html" href="' + links[i] + '"/>\n'
        output += '      <link href="' + messages[i].image_link + '" rel="enclosure"/>\n'
        output += '      <title>' + messages[i].desc + '</title>\n'
        output += '      <summary></summary>\n'
        output += '      <content type="html">\n'
        output += '        &lt;a href="' + messages[i].link + '\"&gt;&lt;img src=\"' + messages[i].image_link + '" /&gt;&lt;/a&gt;\n'
        output += '      </content>\n'
        output += '      <author>\n'
        output += '        <name>' + messages[i].author + '</name>\n'
        output += '        <uri>' + messages[i].author_link + '</uri>\n'
        output += '      </author>\n'
        output += '    </entry>\n'

    output += '</feed>\n'

    with open(path, 'w') as source:
        source.write(output.encode('utf-8'))


main_link = 'http://vk.com/photos279216051'

params_dict = {'messages': []}

full_html = make_html_obj_from(main_link)

params_dict['feed caption'] = full_html.xpath('//title/text()')[0].split('|')[0].strip()

links = parse_image_blocks(full_html.xpath('//div[@class="photo_row"]'))

for link in links:
    params_dict['messages'].append(parse_foto_page(link))
    time.sleep(10)

generate_xml(params_dict['feed caption'], params_dict['messages'], 'result.atom')
