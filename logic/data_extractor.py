import os
import re


def extract(regex_airplane_name):
    print("extracting")

    # '([0-9]+)-(.+)_([0-9]+)-([0-9]+)(.html$)|([0-9]+)-((.+)_*)([0-9]+)(.html$)'

    rootdir = "data/"
    # regex = re.compile(f'(.*zip$)|(.*rar$)|(.*r01$)')
    regex = re.compile(f'([0-9]+)-{regex_airplane_name}(.html$)')

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                print(file)
                seareched_file = open(f'data/{file}', "r", encoding="UTF-8")

                opened_file = seareched_file.read()

                max_speed_regex = re.compile('<li><b>Maximum speed:<\/b> (.*)<\/li>')
                title_regex = re.compile('<title>(.+)<\/title>')

                title = re.findall(title_regex, opened_file)
                max_speed = re.findall(max_speed_regex, opened_file)
                print(title, max_speed)


def compare_airplanes(airplane_1, airplane_2):
    pass
