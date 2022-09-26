# Automatically update your application using GitHub. 

If you need to automatically upload your small application to a server or somewhere else, this project might help.


## Start updater.

1. To start, you need to create a virtual environment in the directory: 
`python -m venv venv`


2. Then go to file ➡️ ```__updater__/settings.py```


3. ```APP = 'test.py'``` If the file to run in some folder, write **not the full path to the script** e.g:
`'dir/run.py'`


4. ```ENVIRONMENT_NAME = 'venv'``` Name of the virtual environment.


5. ```OWNER = 'kanewi11'``` GitHub repository owner.


6. ```REPOSITORY_NAME = 'AutoUpdater'``` Name of the repository to update from.


7. ```UPDATE_DELAY = 120``` Delay in seconds between GitHub checks for the repository.


8. ```PIP = 'pip'``` If you are running pip through a pip3 command, for example, type pip3 here.


9. ```PYTHON = 'python'``` If you run python with python3 for example, type python3.


10. Check that only the `'__updater__'` and `'venv'` directories are in the root directory. **If there are other files there, delete them!**


11. Run `__updater__/main.py`

## Еhe app is still in development
TO DO:
- Checking whether there is a new commit.
- Check bugs