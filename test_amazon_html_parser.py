from unittest import TestCase

from amazon_html_parser import AmazonHTMLParser, remove_string_portion, Review


class TestAmazonHTMLParser(TestCase):
    target = None

    def setUp(self) -> None:
        self._load_file('test_files/html/amazon.html')

    def _load_file(self, filename):
        with open(filename, 'r') as f:
            content = f.read()
        self.target = AmazonHTMLParser()
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

    def test_reviews_ids(self):
        expected_ids = ['R3HPZCT5IDXOV0',
                        'R3V3WQDDK3HGJ6',
                        'R1DBGUZ44N7ML2',
                        'R2AROV2XWDPV21',
                        'RUYOQQNU2YPMY',
                        'RYDYSSM210VTB',
                        'R3KEKF49ZSBHDQ',
                        'R2CLI6GTK6OBJ0',
                        'RL3D1B5C9T3HZ',
                        'RHCFT73ZBPGUS']

        actual_ids = [r.id for r in self.target.reviews]

        self.assertEqual(actual_ids, expected_ids)

    def test_reviews_product_title(self):
        for review in self.target.reviews:
            self.assertEqual('The 5 Love Languages: The Secret to Love that Lasts', review.product_title)
            self.assertEqual('/Love-Languages-Secret-that-Lasts/dp/080241270X/ref=cm_cr_arp_d_product_top?ie=UTF8',
                             review.product_link)

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

    def test_original_star_count(self):
        self._load_file('test_files/html/amazon_mixed_stars.html')
        expected_stars = ['5.0 out of 5 stars',
                          '5.0 out of 5 stars',
                          '5.0 out of 5 stars',
                          '4.0 out of 5 stars',
                          '1.0 out of 5 stars',
                          '1.0 out of 5 stars',
                          '1.0 out of 5 stars',
                          '2.0 out of 5 stars',
                          '1.0 out of 5 stars',
                          '5.0 out of 5 stars']

        actual_star_count = [r.original_stars for r in self.target.reviews]

        self.assertEqual(expected_stars, actual_star_count)

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

    def test_stars(self):
        target = Review()
        target.original_stars = '5.0 out of 5 stars'
        self.assertEqual('5/5', target.stars)
        target.original_stars = '2.0 out of 5 stars'
        self.assertEqual('2/5', target.stars)

    def test_product_id(self):
        target = Review()
        target.product_link = '/Love-Languages-Secret-that-Lasts/dp/080241270X/ref=cm_cr_arp_d_product_top?ie=UTF8'
        self.assertEqual('080241270X',target.product_id)
        target.product_link = '/dp/080241270X/ref=cm_cr_arp_d_product_top?ie=UTF8'
        self.assertEqual('080241270X',target.product_id)