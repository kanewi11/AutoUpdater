# Automatically update your application using GitHub. 

If you need to automatically upload your small application to a server or somewhere else, this project might help.


## Start updater.

1. To start, you need to create a virtual environment in the directory: 
`python -m venv venv`


2. Install requirements `pip install -r requirements.txt`


3. Remove all files and unnecessary directories from the root directory `.gitignore`, `README.md`, `requirements.txt` and so on ➡️🗑. You should be left with two directories `__updater__` and `venv`


4. Then go to file ➡️ ```__updater__/settings.py```


5. ```APP = 'test.py'``` If the file to run in some folder, write **not the full path to the script** e.g:
`'dir/run.py'`


6. ```ENVIRONMENT_NAME = 'venv'``` Name of the virtual environment.


7. ```OWNER = 'kanewi11'``` GitHub repository owner.


8. ```REPOSITORY_NAME = 'AutoUpdater'``` Name of the repository to update from.


9. ```UPDATE_DELAY = 120``` Delay in seconds between GitHub checks for the repository.


10. ```PIP = 'pip'``` If you are running pip through a pip3 command, for example, type pip3 here.


11. ```PYTHON = 'python'``` If you run python with python3 for example, type python3.


12. Check that only the `'__updater__'` and `'venv'` directories are in the root directory. **If there are other files there, delete them!**


13. Run `__updater__/main.py`

## Еhe app is still in development
TO DO:
- Checking whether there is a new commit.
- Check bugs