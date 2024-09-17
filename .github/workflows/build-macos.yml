name: Build macOS App

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build-macos:
    runs-on: macos-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3  # Check out the code from the repository

    - name: Set up Python
      uses: actions/setup-python@v4  # Set up Python
      with:
        python-version: '3.12'  # Replace with the Python version you need

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt  # Install dependencies from requirements.txt

    - name: Install py2app
      run: |
        python -m pip install py2app  # Install py2app

    - name: Build macOS app using py2app
      run: |
        python setup.py py2app  # Build the app using py2app

    - name: Adjust permissions
      run: |
        chmod -R 755 dist/TTrumps.app  # Ensure correct permissions

    - name: Create .dmg file
      run: |
        hdiutil create -volname MyApp -srcfolder dist/ -ov -format UDZO MyApp.dmg  # Package the app into a .dmg

    - name: Upload Artifact
      uses: actions/upload-artifact@v3
      with:
        name: MyApp-dmg
        path: MyApp.dmg
