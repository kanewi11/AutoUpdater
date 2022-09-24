import os.path
from pathlib import Path
from typing import Optional, Any

from git import Repo


from __updater__.exc import MissingKeywordArguments


class Updater(Repo):
    BASE_DIR = Path(__file__).resolve().parent.parent

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
        """Doing a pull and add '__updater__/' in .gitignore file"""
        self.git.pull(self.git_url)
        self._add_updater_in_gitignore()
        self._install_requirements()

    def _install_requirements(self):
        """Install requirements.txt"""
        if not os.path.exists(self.BASE_DIR.joinpath('requirements.txt')):
            return

    def _restart_app(self) -> None:
        """Restart application"""
        ...

    def _add_updater_in_gitignore(self) -> None:
        """Reading in 'a+' may not work adequately, which is why I used two context managers."""

        gitignore_path = self.BASE_DIR.joinpath('.gitignore')
        dir_name = Path(__file__).resolve().parent.name

        with open(gitignore_path, 'r') as gitignore_file:
            if f'{dir_name}/' in gitignore_file.read():  # If the file already contains a '__updater__/', then exit
                return

        with open(gitignore_path, 'a') as gitignore_file:
            gitignore_file.write(f'\n{dir_name}/')  # add in .gitignore file -> '__updater__/'
