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
      uses: actions/checkout@v4 

    - name: Set up Python
      uses: actions/setup-python@v4  
      with:
        python-version: '3.12'  

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt 

    - name: Install py2app
      run: |
        python -m pip install py2app 

    - name: Build macOS app using py2app
      run: |
        python setup.py py2app  

    - name: Adjust permissions
      run: |
        chmod -R 755 dist/TTrumps.app  

    - name: Create .dmg file
      run: |
        hdiutil create -volname MyApp -srcfolder dist/ -ov -format UDZO MyApp.dmg 

    - name: Upload Artifact
      uses: actions/upload-artifact@v3
      with:
        name: MyApp-dmg
        path: MyApp.dmg
