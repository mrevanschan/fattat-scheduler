from rocketry import Rocketry
from rocketry.conds import every
import logging
from logging import config
from services.post_scrapper import __get_recent_posts
import os


config.fileConfig(fname='log.ini')
logging.getLogger('rocketry.task').propagate = False
logging.info("Application Started")
app = Rocketry()


@app.task(every("60 seconds"))
def poll_new_post():
    logging.info("SCHEDULE JOB: POLLING FB")
    for post in __get_recent_posts():
        logging.info(post)


if __name__ == "__main__":
    app.run()
