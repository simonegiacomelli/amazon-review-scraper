from html.parser import HTMLParser
from typing import List
from xml.etree.ElementTree import Element, dump

from puny_html_parser import PunyHTMLParser, print_element


class Review:
    def __init__(self):
        self.title = None


class ReviewPageParser:
    def __init__(self):
        super().__init__()
        self.parser = PunyHTMLParser()
        self.reviews = []

    def feed(self, data):
        self.parser.feed(data)

        reviews_div = [x for x in self.parser.document.findall('.//div') if
                       x.attrib.get('id', '').startswith('customer_review-')]

        self.reviews = [self._div_to_review(div) for div in reviews_div]

    def _div_to_review(self, div):
        children: List[Element] = list(div)
        div_title = children[1]

        a_for_title = div_title.findall('.//a')
        title_span = a_for_title[1].find('.//span')

        review = Review()
        review.title = title_span.text
        return review


def remove_string_portion(content: str, start_marker: str, end_marker: str):
    # remove content that confuses python HTMLParser
    # start_line = '<!--[if IE 6]>'
    # end_line = '<![endif]-->'
    start_idx = content.index(start_marker)
    end_idx = content.index(end_marker, start_idx + len(start_marker))
    return content[:start_idx] + content[end_idx + len(end_marker):]


def remove_confusing(content: str):
    return remove_string_portion(content, '<!--[if IE 6]>', '<![endif]-->')
