from unittest import TestCase

from parse_amazon_html import ReviewPageParser, remove_string_portion


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

    def test_reviews_body(self):
        r9 = self.target.reviews[9]
        self.assertTrue(r9.body.strip().startswith('Do NOT buy this boo'), r9.body)
        r0 = self.target.reviews[0]
        self.assertTrue(r0.body.strip().startswith('I have just started to read this bo'), r0.body)
        r1 = self.target.reviews[1]
        self.assertTrue(r1.body.strip().startswith('I stopped reading at the part wh'), r1.body)
        self.assertTrue(r1.body.strip().endswith('by their bodies; and more.'), r1.body)


class TestRemoveStringPortion(TestCase):
    def test_remove_simple_makers(self):
        content = 'hello<-- dear --> Alice!'
        actual = remove_string_portion(content, '<--', '-->')
        self.assertEqual('hello Alice!', actual)

    def test_remove_same_markers(self):
        content = 'hello -dear-Alice!'
        actual = remove_string_portion(content, '-', '-')
        self.assertEqual('hello Alice!', actual)
