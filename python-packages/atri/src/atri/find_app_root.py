from pathlib import Path
import os
import json
import sys
from . import __version__, app_config_file, supported_virt_types
from .utils.printd import printd

def find_atri_root_dir():
    curr_dir = Path.cwd()
    while True:
        attempt = curr_dir / app_config_file
        if os.path.exists(str(attempt)):
            return curr_dir
        # already at root, cannot go up anymore
        if str(curr_dir) == str(curr_dir.parent):
            return None
        curr_dir = curr_dir.parent

    return None

def find_and_set_app_directory():
    """
    NOTE: use it only inside cli.py or any other entry module.
    This function sets app's root directory as the cwd for the
    running python process.

    It creates atri.app.json file in cwd if not found.
    """
    dir = find_atri_root_dir()
    if dir == None:
        with open(app_config_file, "w") as f:
            content = {"version": __version__}
            f.write(json.dumps(content, indent=2))
    else:
        os.chdir(dir)

def is_supported_virtualenv_type(virt_type):
    return virt_type in supported_virt_types

def get_virtualenv_type():
    try:
        with open(app_config_file, "r") as f:
            content = json.loads(f.read())
            if "virt_type" in content:
                # check if it's a supported virtual env
                virt_type = content["virt_type"]
                if is_supported_virtualenv_type(virt_type):
                    return virt_type
                else:
                    return None
            return None
    except:
        print("Problem reading", app_config_file, "in", Path.cwd())
        printd("[Error]")
        printd(sys.exc_info())
        return None

def is_virtualenv_set():
    if get_virtualenv_type() != None:
        return True
    else:
        return False

def set_virtualenv_type(virt_type: str):
    """
    This function should only be called after find_and_set_app_directory
    has been called. In other words, cwd must be set correctly before
    calling this function. This function also assumes that atri.app.json
    file exists.
    """
    old_content = ""
    with open(app_config_file, "r+") as f:
        old_content = json.loads(f.read())
        f.truncate(0)
    with open(app_config_file, "r+") as f:
        new_content = {"virt_type": virt_type}
        new_content.update(old_content)
        f.write(json.dumps(new_content, indent=2))
