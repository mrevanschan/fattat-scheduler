from rocketry import Rocketry
from rocketry.conds import every
import logging
from logging import config
import os


config.fileConfig(fname='log.ini')
logging.getLogger('rocketry.task').propagate = False
logging.info("Application Started")
app = Rocketry()


@app.task(every("5 seconds"))
def poll_new_post():
    logging.info("SCHEDULE JOB: POLLING FB")
    logging.info(os.environ.get('DATABASE_URL'))


if __name__ == "__main__":
    app.run()
