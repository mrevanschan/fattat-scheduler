import logging
# import os
# import time
from facebook_scraper import get_posts

def scape():
    for post in get_posts("fatchaitat", pages=1):
        logging.info( post["text"])
 

if __name__ == "__main__":
    for post in get_posts("fatchaitat", pages=1):
        print(post["text"])
