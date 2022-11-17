from rocketry import Rocketry
from rocketry.conds import every
import logging
from logging import config
from service.facebook import scrap
# from services.faceook import Facebook

config.fileConfig(fname="log.ini")
logging.getLogger("rocketry.task").propagate = False
logging.info("Application Started")
app = Rocketry()


@app.task(every("1 hour))
def poll_new_post():
    logging.info("SCHEDULE JOB: POLLING FB")
    scrap()

# logging.info(Facebook.scrap_post())
# posts = __get_recent_posts()
# logging.info(f"polled {len(posts)} posts")
# for post in posts:
#     logging.info(post)


if __name__ == "__main__":
    app.run()
