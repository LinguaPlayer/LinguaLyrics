#!/usr/bin/env python3
import platform
import glob
import os
import shutil
import sys

os_type = platform.system()
python_version = str(sys.version_info[0]) + '.' + str(sys.version_info[1])

if os_type == 'Linux':
    path_list = ['/usr/share/pixmaps/lingualyrics.svg',
                 '/usr/share/applications/lingualyrics.desktop',
                 '/usr/local/bin/lingualyrics']

    # Finding LinguaLyrics directories in python dist-packages
    site_packages_path = '/usr/local/lib/python' + python_version + '/dist-packages/'
    pattern = os.path.join(site_packages_path, 'lingualyrics*')
    for folder in glob.glob(pattern):
        path_list.append(folder)

else:
    print('This script is for Linux')
    sys.exit(1)

uid = os.getuid()
if uid != 0:
    print('run this script as root.')
    sys.exit(1)


for path in path_list:
    if os.path.exists(path):
        if os.path.isfile(path):  # if path is for file 
            os.remove(path)  # removing file
        else:
            shutil.rmtree(path)  # removing folder
        print(str(path) + ' is removed!')

print('LinguaLyrics Uninstalled successfully')
