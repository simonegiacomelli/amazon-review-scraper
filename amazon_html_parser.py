from functools import cached_property
from typing import List

from puny_html_parser import PunyHTMLParser


class Review:
    def __init__(self):
        self.id: str = None
        self.title: str = None
        self.body: str = None
        self.product_title: str = None
        self.product_link: str = None
        self.original_stars: str = None
        self.original_date: str = None

    @property
    def date(self) -> str:
        # sample original_date = 'Reviewed in the United States on November 16, 2018'
        tmp = ' '.join(self.original_date.replace(',', '').split(' ')[-3:])
        # tmp should be 'November 16 2018'
        import datetime
        result = datetime.datetime.strptime(tmp, '%B %d %Y').strftime('%Y-%m-%d')
        return result

    @property
    def stars(self) -> str:
        # sample original_stars = '5.0 out of 5 stars'
        return '%s/5' % self.original_stars[:1]

    @property
    def product_id(self) -> str:
        parts = self.product_link.split('/')
        dp_index = parts.index('dp')
        return parts[dp_index + 1]


class ReviewPageParser:
    def __init__(self):
        super().__init__()
        self.parser = PunyHTMLParser()
        self.reviews: List[Review] = []

    def feed(self, data):
        self.parser.feed(data)
        product_element = self.parser.document.find(".//*[@data-hook='product-link']")
        reviews_div = [x for x in self.parser.document.findall(".//*[@data-hook='review']")]
        self.reviews = [self._div_to_review(div, product_element) for div in reviews_div]

    def _div_to_review(self, review_element, product_element):
        review = Review()

        review.product_title = product_element.text
        review.product_link = product_element.attrib.get('href', '')

        review.id = review_element.attrib.get('id', '')

        title_span = review_element.find(".//*[@data-hook='review-title']/span")
        review.title = title_span.text

        body_span = review_element.find(".//*[@data-hook='review-body']/span")
        review.body = body_span.text

        date_span = review_element.find(".//*[@data-hook='review-date']")
        review.original_date = date_span.text

        star_span = review_element.find(".//*[@data-hook='review-star-rating']/span")
        review.original_stars = star_span.text
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
