import csv
import os
import pathlib

from amazon_html_parser import AmazonHTMLParser


def amazon_folder_to_text(folder, f, review_count_limit=None):
    html_file_list = list(pathlib.Path(folder).glob('*.html'))
    # writer = csv.writer(f)
    review_count = 0
    for html_file in html_file_list:
        print('Processing html file: %s' % (html_file))
        parser = AmazonHTMLParser()
        parser.feed(html_file.read_text())
        for r in parser.reviews:
            # writer.writerow((r.id, r.product_id, r.date, r.stars, r.title,))
            f.write('%s\n%s\n\n' % (r.title, r.body))
            review_count += 1
            if review_count_limit is not None and review_count > review_count_limit:
                return

            # amazon_folder_to_text('products/best_sellers/080241270X--Love-Languages-Secret-that-Lasts/three_star',


#                      '080241270X--Love-Languages-Secret-that-Lasts_3star.csv')


best_sellers_folder = 'products/best_sellers'
all_products = os.listdir(best_sellers_folder)

out_folder = 'generated/for_textsight'
os.makedirs(out_folder, exist_ok=True)

for product_folder in all_products:
    with open(out_folder + ('/reviews-%s.txt' % product_folder), 'w', newline='') as f:
        for star in reversed(['five_star', 'four_star', 'three_star', 'two_star', 'one_star']):
            print('computing %s stars' % star)
            amazon_folder_to_text(best_sellers_folder + '/' + product_folder + '/' + star
                                  , f
                                  ,review_count_limit=500)
