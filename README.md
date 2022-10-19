
<div align="center">
    <h1>Automatically update the project from a remote GitHub repository.</h1>
    <a href="https://github.com/kanewi11/AutoUpdater">
        <img src="https://i.gifer.com/origin/e0/e0136905741e0abf318a3bb939a40bdc.gif">
    </a>
</div>

This project tracks new commits in your remote GitHub repository. 
If there is a new commit, the script terminates your application, does a pull, install requirements.txt and restarts the application 🔥

You can fully work out the upgrade methodology in the `__updater__/main.py` file.

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
8. `ENVIRONMENT_NAME = 'venv'` The name of the virtual environment.
9. `OWNER = 'kanewi11'` The owner of the GitHub repository.
10. `REPOSITORY_NAME = 'Diploma'` Name of the repository from which the update will be performed.
11. `UPDATE_DELAY = 120` Delay in seconds between GitHub checks for the repository.
12. You should have this hierarchy before launching:
    ```
    dir_name
    │   README.md
    │   .gitignore
    │   requirements.txt
    │
    └───venv
    │   │   ...
    │   
    └───__updater__
    │   │   __init__.py
    │   │   main.py
    │   │   settings.py
    │   │   updater.py
    │   
    └───.git
        │   ...
    ```
13. Run `__updater__/main.py`. 

After launching, a pull will be made to the main directory from the repository GitHub 
(_which you specified in the settings_). All unnecessary files will be removed. 
Before each update all changes in your files will be erased, be aware of that.