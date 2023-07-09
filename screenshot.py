import os

import validators
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

visited_links = set()


def get_fullpage_screenshot(driver: webdriver.Chrome, url: str, file_name: str = "screenshot1.png", height_margin=0,
                            width_margin=0):
    driver.get(url)
    driver.implicitly_wait(10)
    total_height = driver.execute_script(
        "return Math.max(document.documentElement.clientHeight,document.documentElement.scrollHeight,document.documentElement.offsetHeight,document.body.scrollHeight, document.body.offsetHeight);")
    total_width = driver.execute_script(
        "return Math.max(document.documentElement.clientWidth,document.documentElement.scrollWidth,document.documentElement.offsetWidth,document.body.scrollWidth, document.body.offsetWidth);")

    driver.set_window_size(total_width + width_margin, total_height + height_margin)  # the trick
    driver.save_screenshot(file_name)


def get_current_page_screenshot(driver: webdriver.Chrome, file_name: str = "screenshot1.png", height_margin=0,
                                width_margin=0):
    driver.implicitly_wait(10)
    total_height = driver.execute_script(
        "return Math.max(document.documentElement.clientHeight,document.documentElement.scrollHeight,document.documentElement.offsetHeight,document.body.scrollHeight, document.body.offsetHeight);")
    total_width = driver.execute_script(
        "return Math.max(document.documentElement.clientWidth,document.documentElement.scrollWidth,document.documentElement.offsetWidth,document.body.scrollWidth, document.body.offsetWidth);")

    driver.set_window_size(total_width + width_margin, total_height + height_margin)  # the trick
    driver.save_screenshot(file_name)


def ensure_image_path(file_name, file_extension='.png'):
    count = 0
    original_file = file_name.removesuffix(file_extension)
    while os.path.exists(file_name):
        count += 1
        file_name = original_file + '_' + str(count) + file_extension

    return file_name


def get_all_links_screenshot(driver: webdriver.Chrome, url: str, ss_dir_prefix: str, url_prefix: str = None, ):
    # print(f'scanning: {url} visited: {visited_links}')
    try:
        if url is not None:
            url = url.split('#')[0].split('?')[0].split('&')[0]
        if not validators.url(url) or url in visited_links:
            return set()

        driver.get(url)
        visited_links.add(url)
        image_file_name = ensure_image_path(f'{ss_dir_prefix}/{driver.title}.png')
        # take screenshot of the page
        get_current_page_screenshot(driver, file_name=image_file_name)
        print(f'screenshot take for url: {url} file:{image_file_name}')
        # extract all links on the page
        elems = driver.find_elements(By.TAG_NAME, "a")
        for elem in elems:
            href = elem.get_attribute("href")
            if href is not None and validators.url(href) and (url_prefix is None or href.startswith(url_prefix)):
                get_all_links_screenshot(driver, href, ss_dir_prefix, url_prefix)
    except Exception as e:
        # print(e)
        print(f'Failed SS for url {url}')
        pass


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    web_driver = webdriver.Chrome(options=chrome_options)
    ss_dir = 'screenshots'
    if not os.path.exists(ss_dir):
        os.mkdir(ss_dir)
    get_all_links_screenshot(driver=web_driver, url="https://www.viagra.ca/en-CA", ss_dir_prefix=ss_dir,
                             url_prefix="https://www.viagra.ca")

    print(f'All pages explored: {visited_links}')
    # print(visited_links)

    # get_fullpage_screenshot(driver, "https://www.viatris.com/en", file_name="screenshot2.png")

    # test_fullpage_screenshot(driver, "https://www.geeksforgeeks.org/")
    web_driver.quit()
