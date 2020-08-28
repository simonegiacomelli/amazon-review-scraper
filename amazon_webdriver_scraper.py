import datetime
import shutil
import time
import traceback
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_product(group, product, title):
    for number_of_stars in ['five_star', 'four_star', 'three_star', 'two_star', 'one_star']:
        try:
            scrape_product_star(group, product, title, number_of_stars)
        except Exception as ex:
            print('exception!', str(ex))


def scrape_product_star(group, product, title, number_of_stars):
    output_folder = 'products/%s/%s--%s/%s' % (group, product, title, number_of_stars)
    import os
    os.makedirs(output_folder, exist_ok=True)
    driver = None

    try:

        options = selenium.webdriver.firefox.options.Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path=r"./geckodriver")

        def save_page(page_index: int):
            print('saving', driver.current_url, 'bytes:', len(driver.page_source))
            base_name = f'{output_folder}/page-{page_index}'
            with open(f'{base_name}.html', 'w') as f:
                f.write(driver.page_source)
            driver.save_screenshot(f'{base_name}.screenshot.png')

        wait = WebDriverWait(driver, 10)
        driver.set_window_position(500, 0)

        start_url = 'https://www.amazon.com/product-reviews/%s/' \
                    'ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&refRID=2DVSFP9XYPHHA6NPQ4EY&' \
                    'mediaType=all_contents&pageNumber=1&filterByStar=%s&sortBy=helpful' \
                    % (product, number_of_stars)
        with open(f'{output_folder}/_start_url.txt', 'w') as f:
            f.write(start_url)
        driver.get(start_url)

        nextButtonIdentifier = (By.PARTIAL_LINK_TEXT, 'Next page')
        wait.until(EC.element_to_be_clickable(nextButtonIdentifier))
        save_page(1)
        nextButton = driver.find_element(*nextButtonIdentifier)
        driver.execute_script('arguments[0].scrollIntoView(true);', nextButton)

        for i in range(2, 501):
            nextButton.click()
            wait.until(EC.staleness_of(nextButton))
            try:
                wait.until(EC.element_to_be_clickable(nextButtonIdentifier))
            except selenium.common.exceptions.TimeoutException as ex:
                # last page?
                save_page(i)
                print(ex)
                return
            save_page(i)
            nextButton = driver.find_element(*nextButtonIdentifier)
        return None
    except Exception as ex:
        base_name = f'{output_folder}/_exception'
        driver.save_screenshot(f'{base_name}.screenshot.png')
        with open(f'{base_name}.stacktrace.txt', 'w') as f:
            f.write(traceback.format_exc())
        with open(f'{base_name}.page_source.html', 'w') as f:
            f.write(driver.page_source)
        raise ex
    finally:
        if driver:
            driver.quit()


best_sellers = ['best_sellers', """https://www.amazon.com/Becoming-Michelle-Obama/dp/1524763136/ref=zg_bsar_books_2?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/Educated-Memoir-Tara-Westover/dp/0399590501/ref=zg_bsar_books_3?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/Dog-Man-Creator-Captain-Underpants/dp/1338236598/ref=zg_bsar_books_4?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/Girl-Wash-Your-Face-Believing/dp/1400201659/ref=zg_bsar_books_5?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/Dog-Man-Fetch-22-Creator-Underpants/dp/1338323210/ref=zg_bsar_books_6?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/Wrecking-Ball-Diary-Wimpy-Book/dp/1419739034/ref=zg_bsar_books_7?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/Wonderful-Things-You-Will-Be/dp/0385376715/ref=zg_bsar_books_8?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/School-Zone-Preschool-Pre-Writing-Pre-Reading/dp/0887431453/ref=zg_bsar_books_9?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/Love-Languages-Secret-that-Lasts/dp/080241270X/ref=zg_bsar_books_10?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221
https://www.amazon.com/Where-Crawdads-Sing-Delia-Owens/dp/0735219095/ref=zg_bsar_books_1?_encoding=UTF8&psc=1&refRID=5W2JP51Z9AX9GXV7Q221""".split(
    '\n')]

best_kitchen_and_dining = ['best_kitchen_and_dining',
                           """https://www.amazon.com/DEC012BK-Electric-Scrambled-Vegetables-Dumplings/dp/B00ZGCKLE2/""".split(
                               '\n')]


def extract_product_info(url: str):
    parts = url.split('/')
    dp_index = parts.index('dp')
    return parts[dp_index + 1], parts[dp_index - 1]


group, links = best_kitchen_and_dining
for link in links:
    if len(link.strip()) == 0 or link.startswith('#'):
        continue
    product, title = extract_product_info(link)
    scrape_product(group, product, title)
