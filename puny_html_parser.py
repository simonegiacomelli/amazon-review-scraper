from html.parser import HTMLParser
from typing import Dict
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
            self.last_element.text = str(self.last_element.text or '') + data

    def handle_endtag(self, tag):
        if tag in self.void_elements:
            return

        while tag != self.last_element.tag:
            self.rise_last_element()
            self.assert_last_element_valid(tag)

        if tag == self.last_element.tag:
            self.rise_last_element()
        else:
            raise Exception('-----------endtag=%s last_tag=%s' % (tag, self.last_element))

    def assert_last_element_valid(self, tag):
        if self.last_element is None:
            raise Exception('tag=%s getpos=%s' % (tag, self.getpos()))

    def rise_last_element(self):
        self.last_element = self.parents[self.last_element]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)


def element_to_string(element: Element):
    def dictionary_to_string(d: Dict):
        space = '' if len(d) == 0 else ' '
        return space + ' '.join(['%s="%s"' % (k, v) for k, v in d.items()])

    def get_element_text(ele: Element):
        return '' if ele.text is None else ele.text.replace('\n', '\\n')

    res = []

    def recurse(ele: Element, indent_spaces: int):
        res.append('%s<%s%s>%s' % (' ' * indent_spaces,
                                   ele.tag,
                                   dictionary_to_string(ele.attrib),
                                   get_element_text(ele)
                                   ))
        for child in list(ele):
            recurse(child, indent_spaces + 2)

    recurse(element, 0)
    return '\n'.join(res)


def print_element(element: Element):
    print(element_to_string(element))
