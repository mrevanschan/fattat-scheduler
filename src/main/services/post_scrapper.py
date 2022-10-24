from typing import Iterator


# from service import search_tree


import os
import logging
from logging import config

import facebook_scraper
from facebook_scraper import get_posts, _scraper, Post, extractors
from facebook_scraper.extractors import (PostExtractor)
# from internal_types import MatchingPost
import re

_fb_credentials = (os.environ['FB_USER'], os.environ['FB_PASSWORD'])

_sold_out_regex = re.compile(r'^\*+完')
_payment_link_regex = re.compile(r'^https://wa.me/\d+|^https://forms.gle/')

#
# def skippingMethod(self):
#     logging.debug("SKIPPING EXECUTION")
#     return None
#
#
# extractors.logger.setLevel(logging.ERROR)
# facebook_scraper.logger.setLevel(logging.ERROR)
# PostExtractor.extract_availability = skippingMethod
# PostExtractor.extract_photo_link = skippingMethod
# PostExtractor.extract_image_lq = skippingMethod
# PostExtractor.extract_likes = skippingMethod
# PostExtractor.extract_comments = skippingMethod
# PostExtractor.extract_shares = skippingMethod
# PostExtractor.extract_user_id = skippingMethod
# PostExtractor.extract_username = skippingMethod
# PostExtractor.extract_video = skippingMethod
# PostExtractor.extract_video_thumbnail = skippingMethod
# PostExtractor.extract_video_id = skippingMethod
# PostExtractor.extract_video_meta = skippingMethod
# PostExtractor.extract_is_live = skippingMethod
# PostExtractor.extract_factcheck = skippingMethod
# PostExtractor.extract_share_information = skippingMethod
# PostExtractor.extract_availability = skippingMethod
# PostExtractor.extract_listing = skippingMethod
# PostExtractor.extract_with = skippingMethod


def __get_recent_posts():
    posts = get_posts(
        'fatchaitat',
        page=1,
        credentials=_fb_credentials,
        # cookies="cookies.txt",
        options={
            "allow_extra_requests": False,
            "posts_per_page": 1
        }
    )

    return posts



# def get_potential_posts() -> Iterator[MatchingPost]:
#     incomplete_posts_ids = []
#     matching_posts = []
#     try:
#         for post in __get_recent_posts():
#             # new posts
#             if is_sold_out_post(post):
#                 continue
#             if is_incomplete_post(post):
#                 incomplete_posts_ids.append(post['post_id'])
#             elif is_purchasable_post(post):
#                 # sales post
#                 matching_tags = search_tree.extract_matches(post['post_text'])
#                 if matching_tags != set():
#                     matching_posts.append(
#                         MatchingPost(post['post_id'], matching_tags)
#                     )
#         if incomplete_posts_ids:
#             for post in __get_posts_by_ids(incomplete_posts_ids):
#                 if is_purchasable_post(post):
#                     matching_tags = search_tree.extract_matches(post['post_text'])
#                     if matching_tags != set():
#                         matching_posts.append(
#                             MatchingPost(post['post_id'], matching_tags)
#                         )
#     except Exception as e:
#         logging.error('FB Extraction Error', exc_info=e)
#
#     return matching_posts


def __get_posts_by_ids(post_ids: Iterator[str]) -> Iterator[Post]:
    return get_posts(
        post_urls=post_ids,
        credentials=_fb_credentials,
    )

    if __name__ == "__main__":
        logging.config.fileConfig(fname='log.ini')
    logging.info("Application Started")
    searchTree.refresh_tree()


def is_purchasable_post(post: Post) -> bool:
    return True
    if 'post_link' not in post:
        return False
    return _payment_link_regex.match(post['post_link'])


def is_sold_out_post(post: Post) -> bool:
    return _sold_out_regex.match(post['post_text'])


def is_incomplete_post(post: Post) -> bool:
    return post['post_text'][-1] == '…'
