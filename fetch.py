import requests
from lxml import html


def make_html_obj_from(link):
    import urlparse

    response = requests.get(link)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse.urlparse(response.url))
    parsed_body = html.fromstring(response.content)
    return domain, parsed_body


def generate_xml(links, images, domain, title, path):
    from datetime import datetime

    now = datetime.now()

    output = '<?xml version="1.0" encoding="UTF-8"?>\n'
    output += '  <feed xml:lang="en-US" xmlns="http://www.w3.org/2005/Atom">\n'
    output += '    <id>tag:' + domain + ',2015:/post/atom</id>\n'
    output += '    <link rel="alternate" type="text/html" href="' + main_link + '"/>\n'
    output += '    <link rel="self" type="application/atom+xml" href=""/>\n'
    output += '    <title>' + title + '</title>\n'
    output += '    <updated>' + now.isoformat() + '</updated>\n'

    for i in xrange(len(links)):
        output += '    <entry>\n'
        output += '      <id>tag:' + domain + ',2005:Post/' + images[i].split('/')[-1].split('.')[-2] + '</id>\n'
        output += '      <published>' + now.isoformat() + '</published>\n'
        output += '      <updated>' + now.isoformat() + '</updated>\n'
        output += '      <link rel="alternate" type="text/html" href="' + links[i] + '"/>\n'
        output += '      <link href="' + images[i] + '" rel="enclosure"/>\n'
        output += '      <title>' + images[i].split('/')[-1] + '</title>\n'
        output += '      <summary></summary>\n'
        output += '      <content type="html">\n'
        output += '        &lt;a href="' + links[i] + '\"&gt;&lt;img src=\"' + images[i] + '" /&gt;&lt;/a&gt;\n'
        output += '      </content>\n'
        output += '      <author>\n'
        output += '        <name>' + title + '</name>\n'
        output += '        <uri>' + links[i] + '</uri>\n'
        output += '      </author>\n'
        output += '    </entry>\n'

    output += '</feed>\n'

    with open(path, 'w') as source:
        source.write(output.encode('utf-8'))


main_link = 'http://m.vk.com/photos279216051'

res = make_html_obj_from(main_link)
dom = res[0][:-1]
full_html = res[1]

caption = full_html.xpath('//title/text()')[0].split('|')[0].strip()

blocks = full_html.xpath('//div[@class="photo_row"]')

urls = []
photos = []

for block in blocks:
    l = block.xpath('./a/@href')
    p = block.xpath('./a/img/@src')
    if len(l) == 0 or len(p) == 0:
        print 'wrong block ', block.xpath('./text()')
        continue
    urls.append(dom + l[0].replace('?all=1', ''))
    photos.append(p[0])

urls = full_html.xpath('//div[@class="photo_row"]/a/@href')
urls = map(lambda x: dom + x.replace('?all=1', ''), urls)

photos = full_html.xpath('//img[@class="photo_row_img"]/@src')

generate_xml(urls, photos, dom, caption, 'result.atom')
