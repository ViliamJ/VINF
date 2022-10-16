import os
import re


def extract(regex_airplane_name):
    print("extracting")

    '([0-9]+)-(.+)_([0-9]+)-([0-9]+)(.html$)|([0-9]+)-((.+)_*)([0-9]+)(.html$)'

    rootdir = "data/"
    # regex = re.compile(f'(.*zip$)|(.*rar$)|(.*r01$)')
    regex = re.compile(f'([0-9]+)-{regex_airplane_name}(.html$)')

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                print(file)
                opened_file = open(f'data/{file}', "r", encoding="UTF-8")
                print(opened_file.read())
