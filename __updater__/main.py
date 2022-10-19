""" Example of a function to check for an update and install that update, if there is one. """
import logging
import traceback
from time import sleep

from __updater__.settings import (
    OWNER,
    REPOSITORY_NAME,
    APP,
    ENVIRONMENT_NAME,
    REMOTE_BRANCH_NAME,
    UPDATE_CHECK_DELAY
)
from __updater__.updater import Updater


logging.basicConfig(level=logging.INFO, filename='logs.log', format='%(asctime)s %(levelname)s %(message)s')
logging.info('Starting updater.')

updater = Updater(owner=OWNER,
                  repository_name=REPOSITORY_NAME,
                  app_name=APP,
                  environment_name=ENVIRONMENT_NAME,
                  branch_name=REMOTE_BRANCH_NAME)


def update():
    is_update = updater.check_update()
    if not is_update:
        sleep(UPDATE_CHECK_DELAY)
        return

    updater.kill_app()
    updater.update()
    updater.add_updater_in_gitignore()
    updater.install_requirements()
    updater.run_app()


def main():
    try:
        update()
    except Exception as error:
        logging.error(traceback.format_exc())
        ...
        raise error


if __name__ == '__main__':
    while True:
        main()
