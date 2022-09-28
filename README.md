# Automatically update the application using GitHub. 

## This project can: 
* Track new commits
* Update with pull
* Set requirements.txt 
* Restart the application


## Run the update program.

1. First you need to create a virtual environment in the directory: 
`python -m venv venv`.


2. Set the requirements `pip install -r requirements.txt`.


3. Remove all files and unnecessary directories from the root directory `.gitignore`, `README.md`, `requirements.txt` and so on ➡️🗑. You should be left with two directories `__updater__/` and `venv/`.


4. Then navigate to the file ➡️ `__updater__/settings.py`.


5. `APP = 'test.py'` If the file to run is in some folder, write **relative path to the script**, for example:
`dir/run.py'`.


6. `ENVIRONMENT_NAME = 'venv'` The name of the virtual environment.


7. `OWNER = 'kanewi11'` The owner of the GitHub repository.


8. `REPOSITORY_NAME = 'AutoUpdater'` Name of the repository from which the update will be performed.


9. `UPDATE_DELAY = 120` Delay in seconds between GitHub checks for the repository.


10. `PIP = 'pip'` If you run pip, for example, with pip3, enter pip3 here.


11. `PYTHON = 'python'` If you are running python, for example, using the python3 command, enter python3 here.


12. Check that only the `__updater__/` and `venv/` directories are in the root directory. **If there are other files there, delete them!**.


13. Run `__updater__/main.py`.