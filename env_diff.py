import sys

from env_analyse import get_packages_and_channels

from tabulate import tabulate


def compare_env_files(env_file_1, env_file_2):
    first_file_packages, _ = get_packages_and_channels(env_file_1)
    second_file_packages, _ = get_packages_and_channels(env_file_2)

    first_file_packages_dict = {pkg[0]: pkg[1] for pkg in first_file_packages}
    second_file_packages_dict = {pkg[0]: pkg[1] for pkg in second_file_packages}

    missing_packages = set(first_file_packages_dict.keys()) - set(second_file_packages_dict.keys())
    if missing_packages:
        print(f"\nThe following packages were not found in {env_file_2}:")
        for pkg in missing_packages:
            print(pkg)

    different_versions = []
        
    for pkg in second_file_packages:
        first_file_version = first_file_packages_dict.get(pkg[0])
        if first_file_version != pkg[1]:
            different_versions.append((pkg[0], first_file_version, pkg[1]))
        
    if different_versions:
        print("\nThe following packages have different versions:")
        headers = ["Package", env_file_1, env_file_2]
        print(tabulate(different_versions, headers=headers, tablefmt='pretty'))

    if not missing_packages and not version_mismatch_packages:
        print("\nAll packages are match.")


if __name__ == '__main__':
    compare_env_files(sys.argv[1], sys.argv[2])
