import os
import sys
import yaml


def get_packages_and_channels(envfile):
    filename, file_extension = os.path.splitext(envfile)
    if file_extension == '.txt':
        with open(envfile, 'r') as f:
            packages = [parse_pip_package_string(line) for line in f.read().splitlines()]
            channels = []  # No channels for .txt files
    elif file_extension == '.yml':
        with open(envfile, 'r') as f:
            env_dict = yaml.safe_load(f)
            channels = env_dict.get('channels', [])
            dependencies = env_dict.get('dependencies', [])
            conda_packages = []
            pip_packages = []
        
            for pkg in dependencies:
                if isinstance(pkg, str):
                    conda_packages.append(parse_conda_package_string(pkg))
                elif isinstance(pkg, dict) and 'pip' in pkg:
                    pip_packages.extend([parse_pip_package_string(p) for p in pkg['pip']])
            packages = conda_packages + pip_packages
    else:
        print(f"Unsupported file format: {file_extension}")
        sys.exit(1)
    return packages, channels


def parse_conda_package_string(package_string):
    # Check for channel
    split_on_channel = package_string.split('::')
    if len(split_on_channel) == 2:
        channel, package_string = split_on_channel
    else:
        channel = None

    # Check for version
    if '>=' in package_string:
        split_on_version = package_string.split('>=')
        package_name, package_version = split_on_version
    elif '==' in package_string:
        split_on_version = package_string.split('==')
        package_name, package_version = split_on_version
    elif '=' in package_string:
        split_on_version = package_string.split('=', 1)
        package_name, package_version = split_on_version
        if '=' in package_version:
            package_version = package_version.split('=')[0]
    else:
        package_name = package_string
        package_version = None

    return package_name, package_version, channel


def parse_pip_package_string(package_string):
    channel = 'PyPI'

    # Check for version
    if '>=' in package_string:
        split_on_version = package_string.split('>=')
        package_name, package_version = split_on_version
    elif '==' in package_string:
        split_on_version = package_string.split('==')
        package_name, package_version = split_on_version
    elif '=' in package_string:
        split_on_version = package_string.split('=', 1)
        package_name, package_version = split_on_version
        if '=' in package_version:
            package_version = package_version.split('=')[0]
    else:
        package_name = package_string
        package_version = None

    return package_name, package_version, channel
