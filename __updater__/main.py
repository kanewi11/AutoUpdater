from time import sleep

from __updater__.settings import UPDATE_DELAY
from __updater__.updater import Updater


updater = Updater()


def main():
    updater.restart_app()
    while True:
        if updater.check_update():
            sleep(UPDATE_DELAY)
            continue
        updater.kill_application()
        updater.update()
        updater.add_updater_in_gitignore()
        updater.install_requirements()
        updater.run_application()


if __name__ == '__main__':
    main()
