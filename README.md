# Automatically update the application using GitHub. 

If you are interested in this project, I will be your pull requests.

## This project can: 
* Track new commits
* Update with pull
* Install `requirements.txt`
* Automatically run your application after you run `__updater__/main.py`
* **Automatically restart your application after an update**

Once started, `__updater__/main.py` will automatically create a git repository and make a pull from the one specified in the settings.

## Run the update program.

**Before each update, all your local changes will be overwritten, 
so think ahead and make sure that all the parameters 
that need to be changed in production are put in the environment variables.**

1. Create an empty directory
2. Clone the repository `git clone https://github.com/kanewi11/AutoUpdater.git ./`
3. Creating a virtual environment `python3 -m venv venv`
4. Activating the virtual environment `source venv/bin/activate` 
5. Set the requirements `pip install -r requirements.txt`
6. Then navigate to the file ➡️ `__updater__/settings.py`
7. `APP = 'test.py'` This is the file to run your script, change its name. If the file to run is in some folder, write **relative path to the script**, e.g:
`'dir/run.py'`
8. `ENVIRONMENT_NAME = 'venv'` The name of the virtual environment
9. `OWNER = 'kanewi11'` The owner of the GitHub repository
10. `REPOSITORY_NAME = 'Diploma'` Name of the repository from which the update will be performed
11. `UPDATE_DELAY = 120` Delay in seconds between GitHub checks for the repository
12. `PIP = 'pip'` If you run pip, for example, with pip3, enter `'pip3'` here
13. `PYTHON = 'python'` If you are running python, for example, using the python3 command, enter `'python3'` here
14. Run `__updater__/main.py`