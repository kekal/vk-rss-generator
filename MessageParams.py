class MessageParams(object):

    def __init__(self, link='', desc='', author='', author_link='', image_link=''):
        self._image_link = image_link
        self._author_link = author_link
        self._author = author
        self._desc = desc
        self._link = link

    @property
    def image_link(self):
        return self._image_link

    @image_link.setter
    def image_link(self, value):
        self._image_link = value

    @image_link.deleter
    def image_link(self):
        del self._image_link

    @property
    def author_link(self):
        return self._author_link

    @author_link.setter
    def author_link(self, value):
        self._author_link = value

    @author_link.deleter
    def author_link(self):
        del self._author_link

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @author.deleter
    def author(self):
        del self._author

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @desc.deleter
    def desc(self):
        del self._desc

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @link.deleter
    def link(self):
        del self._link
