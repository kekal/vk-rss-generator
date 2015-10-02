# coding=utf-8
import os


class AtomGenerator(object):
    def __init__(self, params_dict=None, path='result6.atom'):
        self.params_dict = params_dict
        self.path = os.path.join(os.path.dirname(__file__), path)

    def generate_xml(self):
        if self.params_dict is None:
            raise ValueError()
        from datetime import datetime

        now = datetime.now()

        output = '<?xml version="1.0" encoding="UTF-8"?>\n'
        output += '  <feed xml:lang="en-US">\n'  # xmlns="http://www.w3.org/2005/Atom">\n'
        output += '    <id>tag:' + self.params_dict['main_link'] + ':/post/atom</id>\n'
        output += '    <link rel="alternate" type="text/html" href="' + self.params_dict['main_link'] + '"/>\n'
        output += '    <link rel="self" type="application/atom+xml" href=""/>\n'
        output += '    <title>' + self.params_dict['feed caption'] + '</title>\n'
        output += '    <updated>' + now.isoformat() + '</updated>\n'

        messages = self.params_dict['messages']

        for i in xrange(len(messages)):
            output += '    <entry>\n'
            output += '      <id>tag:' + self.params_dict['main_link'] + ',2005:Post/' + \
                      messages[i].image_link.split('/')[-1].split('.')[-2] + \
                      '</id>\n'
            output += '      <published>' + now.isoformat() + '</published>\n'
            output += '      <updated>' + now.isoformat() + '</updated>\n'
            output += '      <link rel="alternate" type="text/html" href="' + messages[i].page_link + '"/>\n'
            output += '      <link href="' + messages[i].image_link + '" rel="enclosure"/>\n'
            output += '      <title>' + messages[i].description + '</title>\n'
            output += '      <summary></summary>\n'
            output += '      <content type="html">\n'
            output += '       ' + messages[i].content + ' &lt;br/&gt; '
            output += '        &lt;a href="' + messages[i].page_link + '\"&gt;&lt;img src=\"' + messages[
                i].image_link + '" /&gt;&lt;/a&gt;\n'
            output += '      </content>\n'
            output += '      <author>\n'
            output += '        <name>' + messages[i].author_name + '</name>\n'
            output += '        <uri>' + messages[i].author_link + '</uri>\n'
            output += '      </author>\n'
            output += '    </entry>\n'

        output += '</feed>\n'

        with open(self.path, 'w') as source:
            source.write(output.encode('utf-8'))
