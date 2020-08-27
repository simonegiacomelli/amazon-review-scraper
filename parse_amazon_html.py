from html.parser import HTMLParser
from typing import List
from xml.etree.ElementTree import Element, dump

from puny_html_parser import PunyHTMLParser, print_element


class Review:
    def __init__(self):
        self.title: str = None
        self.body: str = None


class ReviewPageParser:
    def __init__(self):
        super().__init__()
        self.parser = PunyHTMLParser()
        self.reviews: List[Review] = []

    def feed(self, data):
        self.parser.feed(data)

        reviews_div = [x for x in self.parser.document.findall(".//*[@data-hook='review']")]
        self.reviews = [self._div_to_review(div) for div in reviews_div]

    def _div_to_review(self, review_element):
        review = Review()

        title_span = review_element.find(".//*[@data-hook='review-title']/span")
        review.title = title_span.text

        body_span = review_element.find(".//*[@data-hook='review-body']/span")
        review.body = body_span.text

        # date_span = review_element.find(".//*[@data-hook='review-date']")

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
