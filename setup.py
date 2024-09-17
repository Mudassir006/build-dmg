from setuptools import setup

# Define the script to be turned into an app
APP = ['TTrumps.py']  # Replace with your script name

# Define additional files like images, icons, or other resources
DATA_FILES = ['icon48.png']  # Replace with your resources, if any

# Define options for py2app
OPTIONS = {
    'argv_emulation': True,  # Ensures correct command-line argument handling
    'iconfile': 'icon48.png',  # Path to your app's icon
    'packages': [],  # Include any Python packages your script uses
    'plist': {
        'CFBundleName': 'TTrumps',  # App name
        'CFBundleDisplayName': 'TTrumps',  # Display name
        'CFBundleIdentifier': 'com.yourcompany.ttrumps',  # Replace with your app's identifier
        'CFBundleShortVersionString': '0.1.0',  # App version
        'CFBundleVersion': '0.1.0',  # Build version
        'NSPrincipalClass': 'NSApplication',  # App entry point
        'NSHighResolutionCapable': True,  # Enable retina display support
    },
    'resources': DATA_FILES,  # Add any additional resources (e.g., images, files)
}

# Setup script for py2app
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},  # Pass the py2app options here
    setup_requires=['py2app'],  # py2app is required for this setup
)
