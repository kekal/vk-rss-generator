from StringIO import StringIO
from lxml import etree

from PostParamsContainer import PostParamsContainer


# ----------------------------------------------------------------------

def parse_atom(xml_file):
    params_dict = {'messages': []}

    with open(xml_file) as f:
        xml = f.read()

    root = etree.parse(StringIO(xml)).getroot()
    del xml

    for child in root:
        if child.tag == 'title':
            params_dict['feed caption'] = child.text

        if child.tag != 'entry':
            continue
        entry = child
        published = link = image = desc = author = author_link = content = ''
        for grandchild in entry:
            if grandchild.tag == 'id':
                img_hash = grandchild.text.split('/')
                img_hash = img_hash[-1]
            if grandchild.tag == 'published':
                published = grandchild.text
            if grandchild.tag == 'link':
                if grandchild.attrib['rel'] == 'alternate':
                    link = grandchild.attrib['href']
                else:
                    image = grandchild.attrib['href']
            if grandchild.tag == 'title':
                desc = grandchild.tail
            if grandchild.tag == 'author':
                author = grandchild[0].text
                author_link = grandchild[1].text
            if grandchild.tag == 'content':
                content = grandchild.text

        params_dict['messages'].append(
            PostParamsContainer(link, desc, author, author_link, image, published, img_hash, content))

    return params_dict


if __name__ == "__main__":
    entry_hash_list = parse_atom("result6.atom")
    print entry_hash_list
