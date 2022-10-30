import logging
import time
from urllib import parse

from fake_headers import Headers
from selenium import webdriver

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

no_post_to_scape = 12


class CountChangeCondition(object):
    def __init__(self, locator, length):
        self.locator = locator
        self.length = length

    def __call__(self, driver):
        element = driver.find_elements(*self.locator)
        element_count = len(element)
        if element_count > self.length:
            return element
        else:
            return False


class Facebook:
    @staticmethod
    def quit_driver(driver):
        driver.close(
        )
        driver.quit()

    @staticmethod
    def init_driver():
        try:
            ua = Headers().generate()  # fake user agent
            browser_option = Options()
            browser_option.add_argument('--headless')
            browser_option.add_argument('--disable-extensions')
            browser_option.add_argument('--incognito')
            browser_option.add_argument(f'user-agent={ua}')
            browser_option.add_argument("--no-sandbox");
            browser_option.add_argument("--disable-dev-shm-usage");
            s = Service('/usr/local/bin/chromedriver')
            return webdriver.Chrome(options=browser_option)
        except Exception as ex:
            print(ex)

    @staticmethod
    def scroll_for_post(browser):
        pre_scroll_post_count = len(browser.find_elements(By.CLASS_NAME, '_3drp'))
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
            "lenOfPage;")
        WebDriverWait(browser, 5).until(
            CountChangeCondition((By.CLASS_NAME, "_3drp"), pre_scroll_post_count)
        )
        return len(browser.find_elements(By.CLASS_NAME, '_3drp'))

    @staticmethod
    def scrap_post():
        try:
            URL = "https://m.facebook.com/fatchaitat"

            browser = Facebook.init_driver()
            browser.get(URL)
            logging.info(browser.page_source)

            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "coverPhoto"))
            )

            number_of_posts = Facebook.scroll_for_post(browser)
            while number_of_posts < no_post_to_scape:
                number_of_posts = Facebook.scroll_for_post(browser)
            browser.find_element(By.ID, "popup_xout").click()

            posts = browser.find_elements(By.CLASS_NAME, '_3drp')[:no_post_to_scape]

            # class text_exposed_show
            post_texts = {}
            for post in posts:
                more_btn = post.find_element(By.XPATH, './/span[@class="text_exposed_hide"]//a[text()="More"]')
                url = more_btn.get_attribute("href")
                post_id = parse.parse_qs(parse.urlparse(url).query)['story_fbid'][0]
                action = webdriver.common.action_chains.ActionChains(browser)
                try:
                    action.move_to_element(more_btn)
                    action.perform()
                    more_btn.click()
                    try:
                        more_btn = post.find_element(By.XPATH, './/span[@class="text_exposed_show"]//a[text()="More"]')
                        logging.error("Need to handle")
                    except NoSuchElementException:
                        post_p_tag = post.find_elements(By.XPATH, './/span[@class="text_exposed"]//p')
                        post_texts[post_id] = ''.join(p.text for p in post_p_tag)
                except Exception as e:
                    # do nothing right here
                    logging.error(e)
                    pass
            return post_texts
        except Exception as ex:
            logging.info(f"exception: {ex}")
            print(ex)
        finally:
            browser.close()
            browser.quit()

if __name__ == '__main__':
    print(Facebook.scrap_post())
