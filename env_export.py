import os
import sys
import subprocess


def export_env(envname, filename):
    print(f"Exporting environment {envname} to {filename}...")
    command = f"conda env export -n {envname}"
    print(command)

    try:
        with open(filename, "w") as f:
            subprocess.check_call(command.split(), stdout=f, stderr=f)
        absolute_path = os.path.abspath(filename)
        print(f"Environment {envname} has been successfully exported to {absolute_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")


if __name__ == '__main__':
    export_env(sys.argv[1], sys.argv[2])
