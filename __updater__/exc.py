
class UpdaterError(Exception):
    """ Base class for all package exceptions """


class MissingKeywordArguments(UpdaterError):
    """ Thrown if even one of the arguments in 'Updater.__init__()' is missing. """

    def __str__(self) -> str:
        return "Updater.__init__() missing 1 or 2 required positional keyword arguments: 'owner' and 'repository_name"
