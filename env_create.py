import os
import subprocess
import sys
import yaml
import subprocess

from env_diff import compare_env_files
from env_analyse import get_packages_and_channels
from env_analyse import parse_package_string
from env_export import export_env


def create_env(envname="my_env", pyver=""):
    print(f"Creating environment {envname}...")
    if not pyver:
        command = f"conda create -y -n {envname}"
    else:
        command = f"conda create -y -n {envname} python={pyver}"
    subprocess.check_call(command.split())


def remove_env(envname):
    print(f"Removing environment {envname}...")
    command = f"conda env remove --name {envname}"
    subprocess.check_call(command.split())


def install_package(envname, package_name, package_version, package_channel, default_channels):
    package_with_version = f"{package_name}=={package_version}" if package_version else package_name
    channels = [package_channel] if package_channel else default_channels
    try:
        command = f"conda install -n {envname} {' '.join('-c ' + ch for ch in channels)} {package_with_version} -y"
        subprocess.check_call(command.split())
    except Exception as e:
        print(f"Failed to install {package_with_version} with conda. Retrying without version specification...")
        try:
            command = f"conda install -n {envname} {' '.join('-c ' + ch for ch in channels)} {package_name} -y"
            subprocess.check_call(command.split())
        except Exception as e:
            print(f"Failed to install {package_name} with conda. Retrying with pip...")
            try:
                command = f"conda run -n {envname} pip install {package_name}"
                subprocess.check_call(command.split())
            except Exception as e:
                print(f"Failed to install {package_name} with pip. Exiting.")
                raise e


def main(envfile, envname, pyver):
    try:
        create_env(envname, pyver)
        packages, channels = get_packages_and_channels(envfile)

        for package in packages:
            package_name, package_version, package_channel = package
            try:
                install_package(envname, package_name, package_version, package_channel, channels)
            except Exception as e:
                print(f"Failed to install package: {package_name}")
                raise e  # Reraise the exception to handle it in the outer scope

            export_env(envname, envname + '_new.yml')

        print(f"Environment {envname} created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Cleaning up...")
        remove_env(envname)
        compare_env_files(envfile, f"{envname}_new.yml")  # Assuming the new file has a name like "{envname}_new.yml"


if __name__ == "__main__":
    envfile = sys.argv[1]
    envname = sys.argv[2] if len(sys.argv) > 2 else "my_env"
    pyver = sys.argv[3] if len(sys.argv) > 3 else ""
    main(envfile, envname, pyver)
