from setuptools import setup

APP = ['TTrumps.py']  
DATA_FILES = ['icon48.png']  
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon48.png',  
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
