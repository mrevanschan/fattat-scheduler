import logging
# import os
# import time
from facebook_scraper import get_posts

def scrape():
    try:
        for post in get_posts("fatchaitat", pages=1):
            logging.info( post["text"])
    except Exception as e:
        logging.error("Oops!", e.__class__, "occurred.")
        logging.error(e)

if __name__ == "__main__":
    for post in get_posts("fatchaitat", pages=1):
        print(post["text"])
