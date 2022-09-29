import logging
import traceback
from time import sleep


from __updater__.settings import (
    OWNER,
    REPOSITORY_NAME,
    APP,
    ENVIRONMENT_NAME,
    REMOTE_BRANCH_NAME,
    PIP,
    PYTHON,
    UPDATE_DELAY
)

from __updater__.updater import Updater


logging.basicConfig(level=logging.INFO, filename="logs.log", format="%(asctime)s %(levelname)s %(message)s")
logging.info('Starting updater.')

updater = Updater(owner=OWNER, repository_name=REPOSITORY_NAME, app_name=APP, environment_name=ENVIRONMENT_NAME,
                  branch_name=REMOTE_BRANCH_NAME, pip=PIP, python=PYTHON)


def main():
    """ Example of a function to check for an update and install that update, if there is one. """
    sleep(UPDATE_DELAY)

    update = updater.check_update()
    if not update:
        return

    updater.kill_application()
    updater.update()
    updater.add_updater_in_gitignore()
    updater.install_requirements()
    updater.run_application()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as error:
            logging.error(traceback.format_exc())
