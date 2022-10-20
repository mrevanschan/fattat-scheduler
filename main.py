from rocketry import Rocketry
from rocketry.conds import every
import logging
from logging import config
import time


config.fileConfig(fname='log.ini')
logging.getLogger('rocketry.task').propagate = False
logging.info("Application Started")
app = Rocketry()


@app.task(every("5 seconds"))
def poll_new_post():
    logging.info("SCHEDULE JOB: POLLING FB")
    time.sleep(1)  # Sleep for 3 seconds
    logging.info("COMPLETE")




if __name__ == "__main__":
    app.run()
