from unittest import TestCase

from parse_amazon_html import ReviewPageParser, remove_string_portion, Review


class TestReviewPageParser(TestCase):
    target = None

    def setUp(self) -> None:
        filename = 'amazon.html'
        with open(filename, 'r') as f:
            content = f.read()
        self.target = ReviewPageParser()
        self.target.feed(content)

    def test_reviews_len_10(self):
        actual = len(self.target.reviews)
        self.assertEqual(actual, 10)
        print(self.target.reviews)

    def test_reviews_titles(self):
        expected_titles = ['Just started to read so more rates are possible at the end of reading',
                           'Sexist, heteronormative, triggering and Religious',
                           'Stuck in 1950s ideals',
                           'Don’t buy',
                           'Lame',
                           'Not worth the hype. Sexist and heteronormative.',
                           'eehhh...',
                           'Waste of trees, all you need is the 5 languages',
                           'more pop psych BS',
                           "DON'T WASTE YOUR MONEY. MISLEADING AND DANGEROUS"]

        actual_titles = [r.title for r in self.target.reviews]

        self.assertEqual(actual_titles, expected_titles)

    def test_review_original_date(self):
        expected_strings = ['Reviewed in the United States on November 16, 2018',
                            'Reviewed in the United States on December 8, 2018',
                            'Reviewed in the United States on February 11, 2019',
                            'Reviewed in the United States on November 9, 2018',
                            'Reviewed in the United States on October 17, 2018',
                            'Reviewed in the United States on October 23, 2019',
                            'Reviewed in the United States on August 16, 2019',
                            'Reviewed in the United States on November 27, 2019',
                            'Reviewed in the United States on October 14, 2018',
                            'Reviewed in the United States on March 13, 2018']

        actual_original_date = [r.original_date for r in self.target.reviews]

        self.assertEqual(expected_strings, actual_original_date)

    def test_reviews_body(self):
        self.assert_review(index=9, startswith='Do NOT buy this boo')
        self.assert_review(index=0, startswith='I have just started to read this bo')
        self.assert_review(index=1, startswith='I stopped reading at the part wh')
        r1 = self.target.reviews[1]
        self.assertTrue(r1.body.strip().endswith('by their bodies; and more.'), r1.body)

    def assert_review(self, index, startswith):
        r = self.target.reviews[index]
        error_msg = 'String "%s..." do not start with [%s]' % (r.body[:len(startswith)], startswith)
        self.assertTrue(r.body.strip().startswith(startswith), error_msg)


class TestRemoveStringPortion(TestCase):
    def test_remove_simple_makers(self):
        content = 'hello<-- dear --> Alice!'
        actual = remove_string_portion(content, '<--', '-->')
        self.assertEqual('hello Alice!', actual)

    def test_remove_same_markers(self):
        content = 'hello -dear-Alice!'
        actual = remove_string_portion(content, '-', '-')
        self.assertEqual('hello Alice!', actual)


class TestReview(TestCase):

    def test_date(self):
        target = Review()
        target.original_date = 'Reviewed in the United States on November 16, 2018'
        self.assertEqual('2018-11-16', target.date)
        target.original_date = 'Reviewed in the United States on August 11, 2019'
        self.assertEqual('2019-08-11', target.date)
