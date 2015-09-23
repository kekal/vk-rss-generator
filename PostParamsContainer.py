class PostParamsContainer(object):
    def __init__(self, page_link='', description='', author_name='', author_link='', image_link='', album_name='', time='',
                 photo_hash='', content=''):
        self._image_link = image_link
        self._album_name = album_name
        self._author_link = author_link
        self._author_name = author_name
        self._description = description
        self._page_link = page_link
        self._time = time
        self._photo_hash = photo_hash
        self._content = content

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
    def album_name(self):
        return self._album_name

    @album_name.setter
    def album_name(self, value):
        self._album_name = value

    @album_name.deleter
    def album_name(self):
        del self._album_name

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
    def author_name(self):
        return self._author_name

    @author_name.setter
    def author_name(self, value):
        self._author_name = value

    @author_name.deleter
    def author_name(self):
        del self._author_name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @description.deleter
    def description(self):
        del self._description

    @property
    def page_link(self):
        return self._page_link

    @page_link.setter
    def page_link(self, value):
        self._page_link = value

    @page_link.deleter
    def page_link(self):
        del self._page_link

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @time.deleter
    def time(self):
        del self._time

    @property
    def photo_hash(self):
        return self._photo_hash

    @photo_hash.setter
    def photo_hash(self, value):
        self._photo_hash = value

    @photo_hash.deleter
    def photo_hash(self):
        del self._photo_hash

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @content.deleter
    def content(self):
        del self._content
