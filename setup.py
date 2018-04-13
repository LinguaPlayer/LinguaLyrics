#!/usr/bin/env python3

import os
import sys
import platform
import shutil

# finding os platform
os_type = platform.system()

if os_type == 'Linux':
    from setuptools import setup
    setuptools_available = True
    print(os_type + " detected!")
else:
    print('This script is only work for GNU/Linux or BSD!')
    sys.exit(1)

# Checking dependencies!
not_installed = ''

# python3-requests
try:
    import requests 
    print('python3-requests is found!')
except:
    print('Error : requests is not installed!')
    not_installed = not_installed + 'python3-requests, '


# show warning , if dependencies not installed!
if not_installed != '':
    print('########################')
    print('####### WARNING ########')
    print('########################')
    print('Some dependencies are not installed .It causes some problems for lingua lyrics! : \n')
    print(not_installed + '\n\n')
    print('Read this link for more information: \n')
    print('https://github.com/LinguaPlayer/LinguaLyrics/blob/master/README.md\n\n')
    answer = input('Do you want to continue?(y/n)')
    if answer not in ['y', 'Y', 'yes']:
        sys.exit(1)

if sys.argv[1] == "test":
   print('We have not unit test :)')
   sys.exit('0')

DESCRIPTION = 'Lingua Lyrics'

DATA_FILES = [
    ('/usr/share/applications/', ['resources/lingualyrics.desktop']),]


# finding current directory
cwd = os.path.abspath(__file__)
setup_dir = os.path.dirname(cwd)

#clearing __pycache__
root_pycache = os.path.join(setup_dir, '__pycache__')
src_pycache = os.path.join(setup_dir, 'lingualyrics', '__pycache__')
gui_pycache = os.path.join(setup_dir, 'lingualyrics', 'gui', '__pycache__')
scripts_pycache = os.path.join(setup_dir, 'lingualyrics', 'scripts', '__pycache__')
gui_mainwindow_pycache = os.path.join(setup_dir, 'lingualyrics', 'gui', 'mainwindow', '__pycache__')
scripts_lyricsources_pycache = os.path.join(setup_dir, 'lingualyrics', 'scripts', 'lyricsources', '__pycache__')

for folder in [root_pycache, src_pycache, gui_pycache, scripts_pycache, gui_mainwindow_pycache, scripts_lyricsources_pycache]:
    if os.path.isdir(folder):
        shutil.rmtree(folder)
        print(str(folder) + ' is removed!')


setup(
    name = 'lingualyrics',
    version = '1.0.0',
    license = 'GPL3',
    description = DESCRIPTION,
    long_description = open('README.md').read(),
    include_package_data = True,
    url = 'https://github.com/LinguaPlayer/LinguaLyrics',
    author = 'Habib Kazemi',
    author_email = 'kazemihabib1996@gmail.com',
    maintainer = 'Habib kazemi',
    maintainer_email = 'kazemihabib1996@gmail.com',
    packages = (
        'lingualyrics', 'lingualyrics.scripts', 'lingualyrics.gui',
        'lingualyrics.gui.mainwindow',
        'lingualyrics.scripts.lyricsources'
        ),
    data_files = DATA_FILES,
    entry_points={
        'console_scripts': [
              'lingualyrics = lingualyrics.__main__'
        ]
    }
)

