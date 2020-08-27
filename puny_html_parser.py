from functools import cached_property
from html.parser import HTMLParser
from xml.etree.ElementTree import Element, SubElement


class PunyHTMLParser(HTMLParser):
    # https://html.spec.whatwg.org/multipage/syntax.html#void-elements
    void_elements = {ele for ele in
                     'area, base, br, col, embed, hr, img, input, link, meta, param, source, track, wbr'.split(', ')}

    def error(self, message):
        raise Exception(message)

    def __init__(self):
        super().__init__()
        self.document: Element = None
        self.last_element: Element = None
        self.parents = {}

    @cached_property
    def head(self):
        raise NotImplemented()

    @cached_property
    def body(self):
        raise NotImplemented()

    def handle_starttag(self, tag, attrs):
        di = {k: v for k, v in attrs}

        if self.document is None:
            self.document = Element(tag)
            self.last_element = self.document
            self.parents[self.last_element] = None
        else:
            parent = self.last_element
            ele = SubElement(self.last_element, tag, di)
            self.parents[ele] = parent
            if tag not in self.void_elements:
                self.last_element = ele

    def handle_data(self, data):
        if self.last_element is not None:
            self.last_element.text = data

    def handle_endtag(self, tag):

        while tag != self.last_element.tag:
            parent = self.parents[self.last_element]
            self.last_element = parent

        if tag != self.last_element.tag:
            raise Exception('-----------endtag=%s last_tag=%s' % (tag, self.last_element))
        else:
            parent = self.parents[self.last_element]
            self.last_element = parent
        pass
