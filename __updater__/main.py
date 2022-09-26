from __updater__.updater import Updater
from __updater__.settings import OWNER, REPOSITORY_NAME


def main():
    updater = Updater(owner=OWNER, repository_name=REPOSITORY_NAME)
    updater.kill_application()
    updater.update()
    updater.add_updater_in_gitignore()
    updater.install_requirements()
    updater.run_application()
    updater.update()

if __name__ == '__main__':
    main()
