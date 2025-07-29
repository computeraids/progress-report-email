import subprocess
import os

### GLOBALS DECLARATION; CHANGE TO CONF LATER ###
env_name = "studentemail"
packages = ["Flask", "pywebview"]

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Check to make sure the proper environment exists
envs = subprocess.run("conda env list", shell=True, capture_output=True, text=True).stdout
if env_name not in envs:
    resp = input(f"The conda environment this script is configured to use, {env_name} was not found (you can change the environment in the settings.conf file). Do you want to create it? (y/n)")
    if "y" in resp:
        # this currently creates an empty env; why?
        subprocess.run(f"conda create --name {env_name}", shell=True)
    else:
        exit()

pkgs = subprocess.run(f"conda list -n {env_name}", shell=True, capture_output=True, text=True).stdout
for package in packages:
    if package not in pkgs:
        resp = input(f"{package} could not be found inside {env_name}. Do you want to install it it? (y/n)")
        if "y" in resp:
            subprocess.run(f"conda run -n {env_name} pip install {package}", shell=True)
        else:
            exit()

subprocess.run(f"conda run -n {env_name} python app.py", shell=True)