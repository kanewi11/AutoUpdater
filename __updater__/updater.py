import os.path
import subprocess
from pathlib import Path
from typing import Any

from git import Repo

from __updater__.settings import APP, PYTHON, ENVIRONMENT_NAME, PIP, REMOTE_BRANCH_NAME, OWNER, REPOSITORY_NAME


class Updater(Repo):
    """The class is inherited from the Repo class of the GitPython library.

    This class may:
        - Auto init git repository
        - Install requirements
        - Close your application
        - Run your app
        - Make a Pull from the GitHub repository
        - Add this package to .gitignore"""

    BASE_DIR = Path(__file__).resolve().parent.parent

    PATH_TO_VENV_ACTIVATE = BASE_DIR.joinpath(f'{ENVIRONMENT_NAME}/bin/activate')
    COMMAND_ACTIVATE_VENV = f'source {PATH_TO_VENV_ACTIVATE}'

    PATH_TO_REQUIREMENTS_FILE = BASE_DIR.joinpath('requirements.txt')
    COMMAND_INSTALL_REQUIREMENTS = f'{PIP} install -r {PATH_TO_REQUIREMENTS_FILE}'

    PATH_TO_APP = BASE_DIR.joinpath(APP)
    COMMAND_RUN_APP = f'nohup {PYTHON} {PATH_TO_APP} &'

    COMMAND_KILL_APP = f'pkill -f {APP}'

    owner = OWNER
    repository_name = REPOSITORY_NAME

    def __init__(self, **kwargs: Any) -> None:
        """Create a new Updater instance.

        :param kwargs:
            Keyword arguments serving as additional options to the git-init command"""

        if not os.path.exists(self.BASE_DIR.joinpath('.git')):
            Repo.init(path=self.BASE_DIR, **kwargs)

        super().__init__(path=self.BASE_DIR)

        self.url = f'https://github.com/{self.owner}/{self.repository_name}.git'

        if not self.remotes:
            self.create_remote(REMOTE_BRANCH_NAME, self.url)

    def update(self, **kwargs: Any) -> None:
        """ Doing hard reset and pull
        :param kwargs:
            Additional arguments to be passed to git-pull"""

        self.git.reset('--hard')
        self.git.pull(self.url, **kwargs)

    def check_update(self) -> bool:
        """ Checking local commit and remote commit """
        try:
            local_last_commit = self.commit().hexsha
        except ValueError:
            return False

        remote = self.remotes[0]
        remote_last_commit = remote.fetch()[0].commit.hexsha
        return remote_last_commit == local_last_commit

    def restart_app(self):
        """ Restarting application """
        self.kill_application()
        self.run_application()

    def install_requirements(self) -> None:
        """ Install requirements.txt """
        if not os.path.exists(self.PATH_TO_REQUIREMENTS_FILE):
            return

        subprocess.run(self._get_command_in_venv(self.COMMAND_INSTALL_REQUIREMENTS), shell=True)

    def kill_application(self) -> None:
        """ Kill application """
        subprocess.run(self.COMMAND_KILL_APP, shell=True)

    def run_application(self) -> None:
        """ Run application """
        subprocess.call(self._get_command_in_venv(self.COMMAND_RUN_APP), shell=True)

    def _get_command_in_venv(self, command: str) -> str:
        """Returns the command to be executed in the virtual environment
        :param command:
            The command to be executed in the virtual environment

        :return:
            The command with the execution of the virtual environment
            activation and the command that was passed to this method"""
        return ';'.join([self.COMMAND_ACTIVATE_VENV, command])

    def add_updater_in_gitignore(self) -> None:
        """ Reading in 'a+' may not work adequately, which is why I used two context managers """

        gitignore_path = self.BASE_DIR.joinpath('.gitignore')
        dir_name = Path(__file__).resolve().parent.name

        with open(gitignore_path, 'r') as gitignore_file:
            if f'{dir_name}/' in gitignore_file.read():  # If the file already contains a '__updater__/', then return
                return

        with open(gitignore_path, 'a') as gitignore_file:
            gitignore_file.write(f'\n{dir_name}/')  # add in .gitignore file -> '__updater__/'
