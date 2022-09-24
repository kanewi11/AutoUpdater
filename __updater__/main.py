from __updater__.updater import Updater
from __updater__.settings import OWNER, REPOSITORY_NAME


def main():
    updater = Updater(repository_name=REPOSITORY_NAME)
    updater.update()


if __name__ == '__main__':
    main()
