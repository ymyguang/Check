@echo off
IF EXIST flag.ini ( python BigXuoXi.py ) ELSE (     
    echo "First run, install the required environment"
    pip install -r requirements.txt
    python BigXuoXi.py
    echo "Don't delete the file!">flag.ini )
