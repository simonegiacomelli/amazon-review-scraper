from html.parser import HTMLParser

from puny_html_parser import PunyHTMLParser


class Review:
    def __init__(self):
        self.title = None


class ReviewPageParser:
    def __init__(self):
        super().__init__()
        self.parser = PunyHTMLParser()
        self.tag_count = 0
        self.reviews = []

    def feed(self, data):
        self.parser.feed(data)
        reviews_div = [self.parser.document.findall('[div]')]

        self.reviews = reviews_div

    def handle_starttag(self, tag, attrs):
        self.tag_count += 1
        di = {k: v for k, v in attrs}
        if tag == 'span' and self.title_coming:
            self.start_pos = self.getpos()
            return

        self.title_coming = tag == 'a' and di.get('data-hook', '') == 'review-title'

        if tag != 'div':
            return
        id: str = di.get('id', '')
        if not id.startswith('customer_review-'):
            return
        self.review = Review()
        self.reviews.append(self.review)

        if not ('data-hook', 'review') in attrs:
            return
        # print(attrs)
        # di = {k: v for k, v in attrs}
        # if 'data-src' not in di:
        #     return
        # data_src = str(di['data-src']).lower()
        # if not data_src.endswith('_360.mp4'):
        #     return
        # self.start_pos = self.getpos()
        # self.attrs = di

    def handle_endtag(self, tag):
        if self.title_coming and tag == 'span':
            self.review.title = (self.start_pos, self.getpos())
        pass

        # print(f'END: {tag} pos:{self.getpos()}')
        # if self.start_pos and tag == 'div':
        #     self.locations.append((self.start_pos, self.getpos(), self.attrs))
        #     self.start_pos = None

    def unknown_decl(self, data):
        print(f'ukn {data} pos:{self.getpos()}')

    def handle_comment(self, data):
        pass
        # print(f'comment {data} pos:{self.getpos()}')


def remove_string_portion(content: str, start_marker: str, end_marker: str):
    # remove content that confuses python HTMLParser
    # start_line = '<!--[if IE 6]>'
    # end_line = '<![endif]-->'
    start_idx = content.index(start_marker)
    end_idx = content.index(end_marker, start_idx + len(start_marker))
    return content[:start_idx] + content[end_idx + len(end_marker):]


def remove_confusing(content: str):
    return remove_string_portion(content, '<!--[if IE 6]>', '<![endif]-->')
