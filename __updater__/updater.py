import os.path
import subprocess
from pathlib import Path
from typing import Optional, Any

from git import Repo

from __updater__.exc import MissingKeywordArguments
from __updater__.settings import APP, PYTHON, ENVIRONMENT_NAME, PIP


class Updater(Repo):
    """The class is inherited from the Repo class of the GitPython library.

    This class may:
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
    COMMAND_RUN_APP = f'{PYTHON} {PATH_TO_APP}'

    COMMAND_KILL_APP = f'pkill -f {APP}'

    def __init__(self, owner: Optional[str] = None, repository_name: Optional[str] = None, **kwargs: Any) -> None:
        """Create a new Updater instance.

        :param owner:
            GitHub repository owner -> https://github.com/kanewi11
            owner = 'kanewi11'.

        :param repository_name:
            GitHub repository name -> https://github.com/kanewi11/MoviePlanet
            repository_name = 'MoviePlanet'.

        :param kwargs:
            - If git is not initialized, you can pass the keyword arguments
            of the magic init(...) method of the Repo class here.
            - If git is initialized, you can pass the keyword arguments
            of the __init__(...) magic method of the Repo class here. """

        if not os.path.exists(self.BASE_DIR.joinpath('.git')):
            self.init(path=self.BASE_DIR, **kwargs)
        elif owner is None or repository_name is None:
            raise MissingKeywordArguments

        super().__init__(path=self.BASE_DIR, **kwargs)

        self.owner = owner
        self.repository_name = repository_name
        self.git_url = f'https://github.com/{owner}/{repository_name}.git'

    def update(self) -> None:
        """Doing a pull"""
        self.git.pull(self.git_url)

    def install_requirements(self) -> None:
        """Install requirements.txt"""
        if not os.path.exists(self.PATH_TO_REQUIREMENTS_FILE):
            return

        subprocess.run(self._get_command_in_venv(self.COMMAND_INSTALL_REQUIREMENTS), shell=True)

    def kill_application(self) -> None:
        """Kill application"""
        subprocess.run(self.COMMAND_KILL_APP, shell=True)

    def run_application(self) -> None:
        """Run application"""
        subprocess.run(self._get_command_in_venv(self.COMMAND_RUN_APP), shell=True)

    def _get_command_in_venv(self, command: str) -> str:
        """Returns the command to be executed in the virtual environment.

        :param command:
            The command to be executed in the virtual environment.
        :return:
            The command with the execution of the virtual environment
            activation and the command that was passed to this method."""
        return ';'.join([self.COMMAND_ACTIVATE_VENV, command])

    def add_updater_in_gitignore(self) -> None:
        """Reading in 'a+' may not work adequately, which is why I used two context managers."""

        gitignore_path = self.BASE_DIR.joinpath('.gitignore')
        dir_name = Path(__file__).resolve().parent.name

        with open(gitignore_path, 'r') as gitignore_file:
            if f'{dir_name}/' in gitignore_file.read():  # If the file already contains a '__updater__/', then return
                return

        with open(gitignore_path, 'a') as gitignore_file:
            gitignore_file.write(f'\n{dir_name}/')  # add in .gitignore file -> '__updater__/'
