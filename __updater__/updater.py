import os.path
import shutil
import subprocess
from pathlib import Path
from typing import Any, Union, Optional

from git import Repo, FetchInfo
from git.util import IterableList
from git.exc import GitCommandError


class Updater(Repo):
    """The class is inherited from the Repo class of the GitPython library.

    This class may:
        - Auto init git repository
        - Install requirements
        - Close your application
        - Run your app
        - Make a Pull from the GitHub repository
        - Add this package to .gitignore

    Before each update, all your local changes will be overwritten,
    so think ahead and make sure that all the parameters
    that need to be changed in production are put in the environment variables."""

    BASE_DIR = Path(__file__).resolve().parent.parent
    DESIRED_DIRECTORIES = [Path(__file__).resolve().parent.name, '.git']
    PATH_TO_GIT = BASE_DIR.joinpath('.git')

    def __init__(self, owner: str, repository_name: str, app_name: str, environment_name: str = 'venv',
                 branch_name: str = 'main', pip: str = 'pip',  python: str = 'python', **kwargs: Any) -> None:
        """Create a new Updater instance
        :param owner:
            GitHub repository owner. Example: https://github.com/{kanewi11}/AutoUpdater
        :param repository_name:
            GitHub repository name. Example: https://github.com/kanewi11/{AutoUpdater}
        :param app_name:
            The name of the file to run your application
        :param environment_name:
            Name of your virtual environment
        :param branch_name:
            The master GitHub branch
        :param pip:
            pip command
        :param python:
            python command
        :param kwargs:
            Keyword arguments serving as additional options to the git-init command"""

        self.owner = owner
        self.repository_name = repository_name
        self.url = f'https://github.com/{self.owner}/{self.repository_name}.git'

        repo_url = Repo(path=self.BASE_DIR).remotes[0].url
        if repo_url != self.url:
            self._delete_git()

        if not os.path.exists(self.PATH_TO_GIT):
            Repo.init(path=self.BASE_DIR, **kwargs)

        super().__init__(path=self.BASE_DIR)

        self.path_to_venv_activate = self.BASE_DIR.joinpath(f'{environment_name}/bin/activate')
        self.command_activate_venv = f'source {self.path_to_venv_activate}'
        self.path_to_requirements_file = self.BASE_DIR.joinpath('requirements.txt')
        self.command_install_requirements = f'{pip} install -r {self.path_to_requirements_file}'
        self.path_to_app = self.BASE_DIR.joinpath(app_name)
        self.command_run_app = f'nohup {python} {self.path_to_app} &'
        self.command_kill_app = f'pkill -f {app_name}'
        self.DESIRED_DIRECTORIES.append(environment_name)

        if not self.remotes:
            self.create_remote(branch_name, self.url)

        self.kill_application()
        self.run_application()

    def update(self, **kwargs: Any) -> IterableList[FetchInfo]:
        """ Doing hard reset and pull
        :param kwargs:
            Additional arguments to be passed to git-pull
        :return: Please see 'fetch' method"""

        self.git.reset('--hard')
        try:
            return self.git.pull(self.url, **kwargs)
        except GitCommandError:
            self._delete_files()
            return self.git.pull(self.url, **kwargs)

    def check_update(self) -> bool:
        """Check new updates
        :return:
            If True is returned, there is an update.
            If it returns False, there is no update."""

        try:
            local_last_commit = self.commit().hexsha
        except ValueError:
            return True

        remote = self.remotes[0]
        remote_last_commit = remote.fetch()[0].commit.hexsha
        return remote_last_commit != local_last_commit

    def install_requirements(self) -> Union[None, 'subprocess.CompletedProcess']:
        """ Install requirements.txt
        :return: None if not exist file requirements.txt or if exit 'subprocess.CompletedProcess'"""
        if not os.path.exists(self.path_to_requirements_file):
            return
        return subprocess.run(self._get_command_in_venv(self.command_install_requirements), shell=True)

    def kill_application(self, custom_command_kill_app: Optional[str] = None) -> 'subprocess.CompletedProcess':
        """Kill application
        :param custom_command_kill_app:
            Your custom application termination command. Initially -> 'nohup app_name.py &'
        :return: 'subprocess.CompletedProcess'"""
        command_kill_app = custom_command_kill_app or self.command_kill_app
        return subprocess.run(command_kill_app, shell=True)

    def run_application(self, custom_command_run_app: Optional[str] = None) -> None:
        """Run application
        :param custom_command_run_app:
            Your custom application launch command. Initially -> 'pkill -f app_name.py'"""
        command_run_app = custom_command_run_app or self.command_run_app
        subprocess.call(self._get_command_in_venv(command_run_app), shell=True)

    def _get_command_in_venv(self, command: str) -> str:
        """ Returns the command to be executed in the virtual environment
        :param command:
            The command to be executed in the virtual environment
        :return:
            The command with the execution of the virtual environment
            activation and the command that was passed to this method"""
        return f'{self.command_activate_venv};{command}'

    def add_updater_in_gitignore(self) -> None:
        """Add __ updater__ in .gitignore file.
        Reading through 'a+' may not work adequately, so I used two context managers """
        gitignore_path = self.BASE_DIR.joinpath('.gitignore')
        dir_name = Path(__file__).resolve().parent.name

        with open(gitignore_path, 'r') as gitignore_file:
            if f'{dir_name}/' in gitignore_file.read():
                return

        with open(gitignore_path, 'a') as gitignore_file:
            gitignore_file.write(f'\n{dir_name}/')

    def _delete_files(self) -> None:
        """ Delete all file in root dir """
        all_files = self.BASE_DIR.iterdir()
        for file in all_files:
            if file.name in self.DESIRED_DIRECTORIES:
                continue
            shutil.rmtree(file) if Path.is_dir(file) else Path.unlink(file)

    def _delete_git(self) -> None:
        """Deleting a git dir"""
        Path.exists(self.PATH_TO_GIT) and shutil.rmtree(self.PATH_TO_GIT)
